from llama_cpp import Llama
from src.configs.config import CONTEXT_SIZE, FUNCTION_CALLING_MODEL_FILE_PATH


function_calling_llm = Llama(
    model_path=FUNCTION_CALLING_MODEL_FILE_PATH,
    n_ctx=CONTEXT_SIZE,
    n_gpu_layers=-1,
    verbose=False,
    embedding=False
)