from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple


def _message_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
        return "\n".join(texts)
    return str(content)


def estimate_tokens(messages: List[Dict[str, Any]], model_name: Optional[str] = None) -> int:
    text = "\n".join(f"{m.get('role', 'user')}: {_message_text(m.get('content', ''))}" for m in messages)
    try:
        import tiktoken  # type: ignore

        encoding = tiktoken.encoding_for_model(model_name or "gpt-4o-mini")
        return len(encoding.encode(text))
    except Exception:
        return max(1, len(text) // 4)


def _memory_message(memory_block: str) -> Dict[str, Any]:
    memory_text = f"[BEGIN MEMORY]\n{memory_block or ''}\n[END MEMORY]"
    return {"role": "user", "content": [{"type": "text", "text": memory_text}]}


def build_budgeted_messages(
    base_messages: List[Dict[str, Any]],
    history_messages: List[Dict[str, Any]],
    memory_block: str,
    budget_tokens: int,
    model_name: Optional[str],
    reserve_for_output_tokens: int = 256,
    distractor: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if distractor:
        memory_block = f"{memory_block}\n\n[DISTRACTOR]\n{distractor}" if memory_block else f"[DISTRACTOR]\n{distractor}"

    system_messages = [m for m in base_messages if m.get("role") == "system"]
    non_system_base = [m for m in base_messages if m.get("role") != "system"]
    memory_msg = _memory_message(memory_block)

    available_budget = max(1, budget_tokens - reserve_for_output_tokens)

    min_keep = history_messages[-2:] if len(history_messages) >= 2 else history_messages[:]
    selected_history = history_messages[:]

    def _assemble(curr_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [*system_messages, memory_msg, *curr_history, *non_system_base]

    final_messages = _assemble(selected_history)
    while estimate_tokens(final_messages, model_name) > available_budget and len(selected_history) > len(min_keep):
        selected_history.pop(0)
        final_messages = _assemble(selected_history)

    stats = {
        "input_tokens_est": estimate_tokens(final_messages, model_name),
        "memory_tokens_est": estimate_tokens([memory_msg], model_name),
        "dropped_history_messages_count": max(0, len(history_messages) - len(selected_history)),
        "budget_tokens": budget_tokens,
        "reserve_for_output_tokens": reserve_for_output_tokens,
    }
    return final_messages, stats
