
from src.prompts.prompt import build_function_calling_prompt
from src.configs.config import stop_words
import re

def parse_functions(input_str):
    # Regex to match function calls
    func_pattern = re.compile(r'(\w+)\(([^)]*)\)')

    # Split the string by ';' not enclosed in quotes
    func_calls = re.split(r';(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)', input_str)

    result = []

    for func_call in func_calls:
        match = func_pattern.search(func_call)
        if match:
            func_name = match.group(1)
            args_str = match.group(2)

            # Split the arguments by ',' not enclosed in quotes
            args = re.split(r',(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)', args_str)

            # Parse each argument
            arg_dict = {}
            for arg in args:
                key, value = arg.split('=')
                key = key.strip()

                # Try to interpret the value correctly
                if value.startswith("'") and value.endswith("'"):
                    arg_dict[key] = value.strip("'")
                elif value.startswith('"') and value.endswith('"'):
                    arg_dict[key] = value.strip('"')
                elif value.isdigit():
                    arg_dict[key] = int(value)
                else:
                    # Add more type parsing as needed
                    arg_dict[key] = value

            result.append({func_name: arg_dict})
    transformed_list = []
    for func_dict in result:
        for func_name, args in func_dict.items():
            transformed_list.append({"function_name": func_name, "args": args})
    return transformed_list


def service_provider(model, query):
    prompt = build_function_calling_prompt(query)
    result = model.create_completion(
        prompt,
        stream=False,
        max_tokens=1024,
        stop= stop_words,
        temperature=0,
    )
    answer = result["choices"][0]["text"]
    parts = answer.split("Call: ")
    answer = parts[1] if len(parts) > 1 else ""
    functions = parse_functions(answer)
    return functions
    
