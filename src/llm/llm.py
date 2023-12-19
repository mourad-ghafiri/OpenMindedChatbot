from llama_cpp import Llama
from src.configs.config import CONTEXT_SIZE, LLM_MODEL_FILE_PATH


llm = Llama(
    model_path=LLM_MODEL_FILE_PATH,
    n_ctx=CONTEXT_SIZE,
    n_gpu_layers=-1,
    verbose=False,
    embedding=False
)
