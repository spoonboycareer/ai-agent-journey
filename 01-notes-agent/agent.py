import os
import json
import requests
from dotenv import load_dotenv

from tools import TOOLS_SPEC, AVAILABLE_TOOLS

load_dotenv("../.env")

CHAT_URL = os.getenv("CHAT_URL")
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}


def call_model(messages, tools=None):
    payload = {"model": MODEL, "messages": messages, "stream": False}
    if tools:
        payload["tools"] = tools
    response = requests.post(CHAT_URL, headers=HEADERS, json=payload, timeout=60)
    print("Response status code: ", response.status_code)
    return response.json()


def execute_tool(name: str, args: dict) -> str:
    if name not in AVAILABLE_TOOLS:
        return f"Error: unknown tool {name}."

    try:
        return str(AVAILABLE_TOOLS[name](**args))
    except TypeError as e:
        return f"Error: bad arguments for {name}: {e}"
    except Exception as e:
        return f"Error: {name} failed: {e}"


def run_agent(user_question: str, max_steps: int = 5, verbose: bool = True) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that manages the user's notes. "
                "Use tools whenever they help - don't guess at note contents"
                "or file listing, always check first. If a tool returns an "
                "error, read it an adjust your next action accordingly."
            ),
        },
        {"role": "user", "content": user_question},
    ]

    for step in range(max_steps):
        data = call_model(messages=messages, tools=TOOLS_SPEC)
        message = data["choices"][0]["message"]
        messages.append(message)

        tool_calls = message.get("tool_calls")

        if not tool_calls:
            return message["content"]

        if verbose:
            print(f"\n[step {step + 1}] {len(tool_calls)} tool call(s) requested: ")

        for tool_call in tool_calls:
            tool_name = tool_call["function"]["name"]
            raw_str_args = tool_call["function"]["arguments"] or "{}"
            try:
                raw_args = json.loads(raw_str_args)
            except json.JSONDecodeError:
                result = f"Error: malformed JSON argument: {raw_str_args!r}"
            else:
                tool_spec = next(
                    t for t in TOOLS_SPEC if t["function"]["name"] == tool_name
                )
                allowed_args = (
                    tool_spec["function"].get("parameters", {}).get("properties", {})
                )
                tool_args = {
                    k: raw_args[k] for k in (raw_args.keys() & allowed_args.keys())
                }

                if verbose:
                    print(f"    calling tool {tool_name} with args {tool_args}")

                result = execute_tool(tool_name, tool_args)

                if verbose:
                    print(f"    -> {result}")

            messages.append(
                {"role": "tool", "tool_call_id": tool_call["id"], "content": result}
            )

    return "Reached max steps without a final answer - the model may be stuck looping."
