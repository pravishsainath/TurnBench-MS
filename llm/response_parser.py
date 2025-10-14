import re
from typing import Tuple, Optional

from utils.errors import ResponseFormatError
from utils.logger import setup_logger

logger = setup_logger("ResponseParser", "INFO")

class ResponseParser:
    """
    used to extract structured information from LLM responses
    """
    
    @staticmethod
    def extract_proposal(response: str, with_reasoning: bool = True) -> Tuple[Optional[str], str]:
        """extract reasoning and proposal code from response"""
        reasoning = None
        blue_value = None
        yellow_value = None
        purple_value = None
        choice_tag_match = None

        # find <CHOICE> tag position
        choice_tag_match = re.search(r"<CHOICE>", response, re.IGNORECASE)

        if choice_tag_match:
            text_after_choice = response[choice_tag_match.end():].strip()
            if text_after_choice.startswith(":"):
                text_after_choice = text_after_choice[1:].strip()
            
            try:
                # find the first BLUE value after <CHOICE> tag
                blue_match = re.search(r"BLUE\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                blue_value = int(blue_match.group(1))
                # find the first YELLOW value after <CHOICE> tag
                yellow_match = re.search(r"YELLOW\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                yellow_value = int(yellow_match.group(1))
                # find the first PURPLE value after <CHOICE> tag
                purple_match = re.search(r"PURPLE\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                purple_value = int(purple_match.group(1))
            except Exception:
                logger.error(f"Proposal stage, cannot convert extracted value to integer. {text_after_choice}")
                raise Exception(f"Cannot convert extracted value to integer.")
                     
        else:
            # if tag is missing, all values remain None
            raise ResponseFormatError("Cannot find <CHOICE> tag in response.")

        # find <REASONING> tag position
        if with_reasoning:
            reasoning_tag_match = re.search(r"<REASONING>", response, re.IGNORECASE)
        
            if reasoning_tag_match:
                reasoning = response[reasoning_tag_match.end():choice_tag_match.start()].strip()
                if reasoning.startswith(":"):
                    reasoning = reasoning[1:].strip()
            else:
                raise ResponseFormatError("Cannot find <REASONING> tag in response.")
            
        return reasoning, f"{blue_value}{yellow_value}{purple_value}"
    
    @staticmethod
    def extract_verifier_choices(response: str, with_reasoning: bool = True) -> Tuple[Optional[str], str]:
        """extract verifier choices from response"""
        reasoning = None
        choice = None
        choice_tag_match = re.search(r"<CHOICE>", response, re.IGNORECASE)
        
        if choice_tag_match:
            text_after_choice = response[choice_tag_match.end():].strip()
            if text_after_choice.startswith(":"):
                text_after_choice = text_after_choice[1:].strip()
            
            if "SKIP" in text_after_choice:
                choice = "SKIP"
            else:
                number_match = re.search(r'\d+', text_after_choice)
                if number_match:
                    choice = int(number_match.group(0))
                else:
                    logger.error(f"Question stage, did not find any choices in response. {text_after_choice}")
                    raise ResponseFormatError("Did not find any choices in response.")
        else:
            raise ResponseFormatError("Cannot find <CHOICE> tag in response.")

        if with_reasoning:  
            reasoning_tag_match = re.search(r"<REASONING>", response, re.IGNORECASE)
            if reasoning_tag_match:
                reasoning = response[reasoning_tag_match.end():choice_tag_match.start()].strip()
                if reasoning.startswith(":"):
                    reasoning = reasoning[1:].strip()
            else:
                raise ResponseFormatError("Cannot find <REASONING> tag in response.")

        return reasoning, choice
    
    @staticmethod
    def extract_deduce(response: str, with_reasoning: bool = True) -> Tuple[Optional[str], str]:
        """extract final guess from response"""
        reasoning = None
        guess = None
        
        # find <CHOICE> tag position
        choice_tag_match = re.search(r"<CHOICE>", response, re.IGNORECASE)

        if choice_tag_match:
            text_after_choice = response[choice_tag_match.end():].strip()
            if text_after_choice.startswith(":"):
                text_after_choice = text_after_choice[1:].strip()

            if "SKIP" in text_after_choice:
                guess = "SKIP"
            else:
                try:
                    blue_match = re.search(r"BLUE\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                    blue_value = int(blue_match.group(1))
                    yellow_match = re.search(r"YELLOW\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                    yellow_value = int(yellow_match.group(1))
                    purple_match = re.search(r"PURPLE\s*=\s*(\d+)", text_after_choice, re.IGNORECASE)
                    purple_value = int(purple_match.group(1))
                except Exception:
                    raise ResponseFormatError(f"Cannot convert extracted values to integers.")
                     
                guess = f"{blue_value}{yellow_value}{purple_value}"
        else:
            raise ResponseFormatError("Cannot find <CHOICE> tag in response.")

        if with_reasoning:
            reasoning_tag_match = re.search(r"<REASONING>", response, re.IGNORECASE)
            if reasoning_tag_match:
                reasoning = response[reasoning_tag_match.end():choice_tag_match.start()]
                if reasoning.startswith(":"):
                    reasoning = reasoning[1:].strip()
            else:
                raise ResponseFormatError("Cannot find <REASONING> tag in response.")
        
        return reasoning, guess