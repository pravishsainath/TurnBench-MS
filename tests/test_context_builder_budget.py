from vbmem.context_builder import build_budgeted_messages


def _msg(role: str, text: str):
    return {"role": role, "content": [{"type": "text", "text": text}]}


def test_budgeted_context_truncates_history():
    base_messages = [_msg("system", "system prompt")]
    history_messages = [_msg("user", f"history {i} " + ("x " * 120)) for i in range(20)]

    final_messages, stats = build_budgeted_messages(
        base_messages=base_messages,
        history_messages=history_messages,
        memory_block='{"state":"ok"}',
        budget_tokens=256,
        model_name="gpt-4o-mini",
        reserve_for_output_tokens=64,
    )

    assert stats["dropped_history_messages_count"] > 0
    assert stats["input_tokens_est"] <= 192
    assert any("[BEGIN MEMORY]" in block["text"] for msg in final_messages for block in msg.get("content", []) if isinstance(block, dict))
