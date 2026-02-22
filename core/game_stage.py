from typing import List, Tuple, Optional

from core.game_session import GameSession
from llm.llm_manager import LLMClient
from llm.response_parser import ResponseParser
from verifier.verifier_manager import VerifierManager
from utils.errors import ResponseFormatError, ResponseNotValidError
from utils.logger import setup_logger
from models.llm import LLMResponseUsageModel
from models.game import (
    ProposalResultModel,
    QuestionResultModel,
    DeduceResultModel
)
from vbmem.context_builder import build_budgeted_messages, estimate_tokens


class GameStage:
    """game stage base class"""

    def __init__(
        self,
        game_session: GameSession,
        llm_client: LLMClient,
        verifier_manager: VerifierManager,
        log_level: int
    ) -> None:
        self.game_session = game_session
        self.llm_client = llm_client
        self.verifier_manager = verifier_manager
        self.logger = setup_logger("GameStages", log_level)

    def execute(self) -> None:
        raise NotImplementedError("subclass must implement this method")

    def _messages_for_call(self):
        memory_block = self.game_session.get_memory_block()
        system_messages = [m for m in self.game_session.messages if m.get("role") == "system"]
        history_messages = [m for m in self.game_session.messages if m.get("role") != "system"]
        distractor = None
        if self.game_session.distractor_mode != "none" and self.game_session.distractor_tokens > 0:
            distractor = "x " * self.game_session.distractor_tokens

        if self.game_session.prompt_context_mode == "budgeted":
            final_messages, stats = build_budgeted_messages(
                base_messages=system_messages,
                history_messages=history_messages,
                memory_block=memory_block,
                budget_tokens=self.game_session.memory_budget_tokens,
                model_name=self.game_session.model_name,
                reserve_for_output_tokens=256,
                distractor=distractor,
            )
        else:
            memory_message = {
                "role": "user",
                "content": [{"type": "text", "text": f"[BEGIN MEMORY]\n{memory_block}\n[END MEMORY]"}],
            }
            final_messages = [*system_messages, memory_message, *history_messages]
            stats = {
                "input_tokens_est": estimate_tokens(final_messages, self.game_session.model_name),
                "memory_tokens_est": estimate_tokens([memory_message], self.game_session.model_name),
                "dropped_history_messages_count": 0,
            }
        self.game_session.update_context_stats(stats)
        return final_messages


class ProposalStage(GameStage):
    def execute(self) -> None:
        step_prompt = self.game_session.game_prompts.proposal_prompt
        self.game_session.add_message("user", step_prompt)

        reasoning, guess_code, model_reasoning = self._handle_proposal()

        self.logger.debug(f"proposal stage, guess_code: {guess_code}")

        self.game_session.update_all_guesses(guess_code)
        self.game_session.update_round_result("proposal",
            ProposalResultModel(
                guess_code=guess_code,
                reasoning=reasoning,
                model_reasoning=model_reasoning
            )
        )

    def _handle_proposal(self, retry_count=0) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        llm_response = self.llm_client.complete(self.game_session.model_name, self._messages_for_call())
        self.game_session.add_message("assistant", llm_response.content)
        self.game_session.update_game_tokens(LLMResponseUsageModel(**llm_response.model_dump()))
        try:
            reasoning, guess_code = ResponseParser.extract_proposal(llm_response.content, self.game_session.game_state.with_reasoning)
        except ResponseFormatError as e:
            self.game_session.update_game_response_with_formatting_error(1)
            if retry_count > 2:
                raise e
            self.logger.debug(f"proposal stage, response format error, retrying, retry_count: {retry_count}")
            self.game_session.add_message("user", self.game_session.game_prompts.not_valid_proposal_format_prompt)
            return self._handle_proposal(retry_count + 1)
        except Exception as e:
            self.logger.debug(f"proposal stage, unknown error: {e}")
            raise e
        return reasoning, guess_code, llm_response.model_level_reasoning_content


class QuestionStage(GameStage):
    def execute(self) -> None:
        tried_verifiers: List[Tuple[str, str]] = []
        question_round_results: List[QuestionResultModel] = []

        for question_round in range(1, 5):
            stage_continue = self._handle_question_round(question_round, tried_verifiers, question_round_results)
            if not stage_continue:
                break

        self.game_session.update_verifier_uses(tried_verifiers)
        self.game_session.update_round_result("question", question_round_results)

    def _handle_question_round(self, question_round, tried_verifiers, question_round_results) -> bool:
        stage_continue = False
        step_prompt = self._prepare_prompt_for_round(question_round, tried_verifiers, question_round_results)
        self.game_session.add_message("user", step_prompt)
        if question_round == 4:
            self.game_session.add_message("assistant", "I will decide whether to proceed to the next round during the Deduce Stage.")
            return stage_continue
        else:
            model_level_reasoning_content, reasoning, verifier_choice = self._handle_model_response()

        verifier_result = None
        if verifier_choice != "SKIP":
            stage_continue = True
            verifier_result = self._get_verifier_result(int(verifier_choice), self.game_session.round_result.proposal.guess_code)
            tried_verifiers.append((str(verifier_choice), verifier_result))
            self.game_session.update_memory_observation(
                str(self.game_session.setup.verifier_ids[int(verifier_choice)]),
                self.game_session.round_result.proposal.guess_code,
                verifier_result,
            )

        question_round_results.append(QuestionResultModel(
            verifier_choice=str(verifier_choice),
            verifier_result=verifier_result,
            reasoning=reasoning,
            model_reasoning=model_level_reasoning_content
        ))
        self.logger.debug(f"question {question_round}, verifier_choice: {verifier_choice}, verifier_result: {verifier_result}")

        return stage_continue

    def _handle_model_response(
        self,
        format_error_retry_count: int = 0,
        not_valid_error_retry_count: int = 0
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        llm_response = self.llm_client.complete(self.game_session.model_name, self._messages_for_call())
        self.game_session.add_message("assistant", llm_response.content)
        self.game_session.update_game_tokens(LLMResponseUsageModel(**llm_response.model_dump()))

        try:
            reasoning, verifier_choice = ResponseParser.extract_verifier_choices(
                llm_response.content, self.game_session.game_state.with_reasoning)
            if verifier_choice != "SKIP":
                self._check_verifier_choice_valid(verifier_choice)
        except ResponseFormatError as e:
            if format_error_retry_count > 2:
                raise e
            self.logger.debug(f"question stage, response format error, retrying, retry_count: {format_error_retry_count}")
            self.game_session.update_game_response_with_formatting_error(1)
            self.game_session.add_message("user", self.game_session.game_prompts.not_valid_question_format_prompt)
            return self._handle_model_response(format_error_retry_count + 1, not_valid_error_retry_count)
        except ResponseNotValidError as e:
            if not_valid_error_retry_count > 2:
                raise e
            self.logger.debug(f"question stage, response not valid error, retrying, retry_count: {not_valid_error_retry_count}")
            self.game_session.update_game_response_with_not_valid_error(1)
            self.game_session.add_message("user", self.game_session.game_prompts.not_valid_verifier_choice_prompt.format(
                verifier_num=verifier_choice
            ))
            return self._handle_model_response(format_error_retry_count, not_valid_error_retry_count + 1)
        except Exception as e:
            self.logger.debug(f"question stage, unknown error: {e}")
            raise e

        return llm_response.model_level_reasoning_content, reasoning, verifier_choice

    def _prepare_prompt_for_round(self, question_round, tried_verifiers, question_round_results) -> str:
        if question_round == 1:
            return self.game_session.game_prompts.first_question_prompt.format(
                verifier_descriptions=self.game_session.verifier_descriptions
            )
        elif len(tried_verifiers) > 0 and len(question_round_results) == len(tried_verifiers):
            last_verifier_choice, last_verifier_result = tried_verifiers[-1]

            if question_round == 4:
                return self.game_session.game_prompts.after_last_question_prompt.format(
                    verifier_num=last_verifier_choice,
                    verifier_result=last_verifier_result
                )
            else:
                return self.game_session.game_prompts.following_question_prompt.format(
                    verifier_num=last_verifier_choice,
                    verifier_result=last_verifier_result
                )
        raise Exception("No valid prompt found")

    def _get_verifier_result(self, verifier_num: int, guess_code: str) -> str:
        if self.game_session.game_state.mode == "classic":
            verifier_result = "PASS" if self.verifier_manager.verify(
                self.game_session.setup.verifier_ids[verifier_num],
                guess_code,
                self.game_session.setup.active_criteria_ids[verifier_num]
            ) else "FAIL"
        else:
            verifier_result = "PASS" if self.verifier_manager.verify(
                self.game_session.setup.nightmare_verifier_ids[verifier_num],
                guess_code,
                self.game_session.setup.nightmare_active_criteria_ids[verifier_num]
            ) else "FAIL"
        return verifier_result

    def _check_verifier_choice_valid(self, verifier_choice) -> None:
        if int(verifier_choice) < 0 or int(verifier_choice) >= len(self.game_session.setup.verifier_ids):
            self.logger.error(f"Verifier choice {verifier_choice} is not valid. Total verifier count: {len(self.game_session.setup.verifier_ids)}")
            raise ResponseNotValidError(f"Verifier choice {verifier_choice} is not valid.")


class DeduceStage(GameStage):
    def execute(self) -> None:
        step_prompt = self.game_session.game_prompts.deduce_prompt
        self.game_session.add_message("user", step_prompt)

        reasoning, submitted_code, model_reasoning = self._handle_deduce()

        guess_correct = None
        count_of_verifier_passed = 0
        if submitted_code:
            guess_correct = self.game_session.check_answer(submitted_code)
            for i, verifier_id in enumerate(self.game_session.setup.verifier_ids):
                is_passed = self.verifier_manager.verify(verifier_id, submitted_code, self.game_session.setup.active_criteria_ids[i])
                if is_passed:
                    count_of_verifier_passed += 1

            result_prompt = self.game_session.game_prompts.deduce_result_prompt.format(
                submitted_code=submitted_code,
                answer=self.game_session.setup.answer,
                is_correct=guess_correct
            )
            self.game_session.add_message("user", result_prompt)
            llm_response = self.llm_client.complete(self.game_session.model_name, self._messages_for_call())
            self.game_session.add_message("assistant", llm_response.content)
            self.game_session.update_game_tokens(LLMResponseUsageModel(**llm_response.model_dump()))

        self.game_session.update_round_result("deduce",
            DeduceResultModel(
                submitted=submitted_code is not None,
                submitted_code=submitted_code,
                guess_correct=guess_correct,
                num_of_verifier_passed=count_of_verifier_passed if submitted_code else None,
                reasoning=reasoning,
                model_reasoning=model_reasoning
            )
        )

        self.logger.debug((
            f"deduce stage completed, submitted: {'Not submitted' if not submitted_code else submitted_code}, "
            f"guess_correct: {'Not submitted' if not submitted_code else 'Correct' if guess_correct else 'Incorrect'}, "
            f"num_of_verifier_passed: {count_of_verifier_passed if submitted_code else 'Not submitted'}"
        ))

    def _handle_deduce(self, retry_count=0) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        llm_response = self.llm_client.complete(self.game_session.model_name, self._messages_for_call())
        self.game_session.add_message("assistant", llm_response.content)
        self.game_session.update_game_tokens(LLMResponseUsageModel(**llm_response.model_dump()))

        try:
            reasoning, submitted_code = ResponseParser.extract_deduce(llm_response.content, self.game_session.game_state.with_reasoning)
        except ResponseFormatError as e:
            if retry_count > 2:
                raise e
            self.game_session.update_game_response_with_formatting_error(1)
            self.logger.debug(f"deduce stage, response format error, retrying, retry_count: {retry_count}")
            self.game_session.add_message("user", self.game_session.game_prompts.not_valid_deduce_format_prompt)
            return self._handle_deduce(retry_count + 1)
        except Exception as e:
            self.logger.debug(f"deduce stage, unknown error: {e}")
            raise e

        return reasoning, None if submitted_code == "SKIP" else submitted_code, llm_response.model_level_reasoning_content
