from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from src.llm.llm import llm
from src.llm.function_calling_llm import function_calling_llm
from src.configs.config import stop_words
from src.prompts.prompt import assistant_prompt_marcoroni, evil_chatbot_prompt_marcoroni
from src.services.service_provider import service_provider
from src.services.search_online_for_information import search_online_for_information
from src.services.fetch_time_information import fetch_time_information
from src.services.evaluate_math_expression import evaluate_math_expression
from src.services.fetch_weather_information import fetch_weather_information
from src.services.no_relevant_function import no_relevant_function
from src.services.execute_terminal_command import execute_terminal_command
import json


app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/")
def read_root():
    return FileResponse(Path("static/index.html"), media_type="text/html")



@app.websocket("/stream_completion")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        message = await websocket.receive_text()
        message = json.loads(message)
        print(message)
        question = message["message"]
        evilMode = message["evilMode"]
        useInternetFunction = message["useInternetFunction"]
        userTimeFunction = message["userTimeFunction"]
        userWeatherFunction = message["userWeatherFunction"]
        userMathFunction = message["userMathFunction"]
        useTerminalFunction = message["useTerminalFunction"]

        context = ""

        if any([useInternetFunction, userTimeFunction, userWeatherFunction, userMathFunction, useTerminalFunction]):
            services = service_provider(function_calling_llm, question)
            print("functions: ", services)
            for function in services:
                service_name = function["function_name"]
                args = function["args"]
                if service_name == "search_online_for_information" and useInternetFunction:
                    context += search_online_for_information(args["query"]) + "\n"
                elif service_name == "fetch_time_information" and userTimeFunction:
                    context += fetch_time_information(args["time_zone_name"], args["city_name"]) + "\n"
                elif service_name == "fetch_weather_information" and userWeatherFunction:
                    context += fetch_weather_information(args["city_name"]) + "\n"
                elif service_name == "evaluate_math_expression" and userMathFunction:
                    context += evaluate_math_expression(args["expression"]) + "\n"
                elif service_name == "execute_terminal_command" and useTerminalFunction:
                    context += execute_terminal_command(args["command"]) + "\n"
                elif service_name == "no_relevant_function":
                    context += no_relevant_function(args["query"]) + "\n"

        if evilMode:
            prompt = evil_chatbot_prompt_marcoroni(question)
        else:
            prompt = assistant_prompt_marcoroni(question, context)

        stream = llm.create_completion(
            prompt,
            stream=True,
            max_tokens=2048,
            stop= stop_words,
            temperature=0.5 if evilMode else 0.0,
        )
        
        result = ""
        for output in stream:
            result += output["choices"][0]["text"]
            await websocket.send_json(
                {"type": "message", "data": output["choices"][0]["text"]}
            )

