import importlib
import sys
import types


def test_base_client_import_and_init_without_network():
    fake_openai = types.ModuleType("openai")

    class DummyOpenAI:
        def __init__(self, api_key=None, base_url=None):
            self.api_key = api_key
            self.base_url = base_url

    fake_openai.OpenAI = DummyOpenAI

    fake_pydantic = types.ModuleType("pydantic")

    class DummyBaseModel:
        pass

    fake_pydantic.BaseModel = DummyBaseModel

    sys.modules.pop("llm.providers.base_client", None)
    sys.modules["openai"] = fake_openai
    sys.modules["pydantic"] = fake_pydantic

    bc = importlib.import_module("llm.providers.base_client")
    client = bc.LLMClient(api_key="dummy", api_key_env_name="OPENAI_API_KEY")

    assert hasattr(client, "client")
