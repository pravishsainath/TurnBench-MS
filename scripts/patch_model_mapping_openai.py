from __future__ import annotations
from pathlib import Path

import yaml

p = Path("configs/model_mapping.yaml")
data = yaml.safe_load(p.read_text())

def ensure(model: str, provider: str, provider_model: str):
    if model not in data or data[model] is None:
        data[model] = {}
    if provider not in data[model]:
        data[model][provider] = provider_model

ensure("gpt-4o-mini", "openai", "gpt-4o-mini")
ensure("gpt-4.1", "openai", "gpt-4.1")

p.write_text(yaml.safe_dump(data, sort_keys=False))
print("Patched", p)
