<<<<<<< HEAD
from open_webui.utils.task import prompt_template, prompt_variables_template
=======
from open_webui.utils.task import prompt_template
>>>>>>> dfef03c8e (同步远程)
from open_webui.utils.misc import (
    add_or_update_system_message,
)

from typing import Callable, Optional
<<<<<<< HEAD
import json


# inplace function: form_data is modified
def apply_model_system_prompt_to_body(
    params: dict, form_data: dict, metadata: Optional[dict] = None, user=None
) -> dict:
=======


# inplace function: form_data is modified
def apply_model_system_prompt_to_body(params: dict, form_data: dict, user) -> dict:
>>>>>>> dfef03c8e (同步远程)
    system = params.get("system", None)
    if not system:
        return form_data

<<<<<<< HEAD
    # Metadata (WebUI Usage)
    if metadata:
        variables = metadata.get("variables", {})
        if variables:
            system = prompt_variables_template(system, variables)

    # Legacy (API Usage)
=======
>>>>>>> dfef03c8e (同步远程)
    if user:
        template_params = {
            "user_name": user.name,
            "user_location": user.info.get("location") if user.info else None,
        }
    else:
        template_params = {}
<<<<<<< HEAD

    system = prompt_template(system, **template_params)

=======
    system = prompt_template(system, **template_params)
>>>>>>> dfef03c8e (同步远程)
    form_data["messages"] = add_or_update_system_message(
        system, form_data.get("messages", [])
    )
    return form_data


# inplace function: form_data is modified
def apply_model_params_to_body(
    params: dict, form_data: dict, mappings: dict[str, Callable]
) -> dict:
    if not params:
        return form_data

    for key, cast_func in mappings.items():
        if (value := params.get(key)) is not None:
            form_data[key] = cast_func(value)

    return form_data


# inplace function: form_data is modified
def apply_model_params_to_body_openai(params: dict, form_data: dict) -> dict:
    mappings = {
        "temperature": float,
        "top_p": float,
        "max_tokens": int,
        "frequency_penalty": float,
<<<<<<< HEAD
        "reasoning_effort": str,
=======
>>>>>>> dfef03c8e (同步远程)
        "seed": lambda x: x,
        "stop": lambda x: [bytes(s, "utf-8").decode("unicode_escape") for s in x],
    }
    return apply_model_params_to_body(params, form_data, mappings)


def apply_model_params_to_body_ollama(params: dict, form_data: dict) -> dict:
<<<<<<< HEAD
    # Convert OpenAI parameter names to Ollama parameter names if needed.
    name_differences = {
        "max_tokens": "num_predict",
=======
    opts = [
        "temperature",
        "top_p",
        "seed",
        "mirostat",
        "mirostat_eta",
        "mirostat_tau",
        "num_ctx",
        "num_batch",
        "num_keep",
        "repeat_last_n",
        "tfs_z",
        "top_k",
        "min_p",
        "use_mmap",
        "use_mlock",
        "num_thread",
        "num_gpu",
    ]
    mappings = {i: lambda x: x for i in opts}
    form_data = apply_model_params_to_body(params, form_data, mappings)

    name_differences = {
        "max_tokens": "num_predict",
        "frequency_penalty": "repeat_penalty",
>>>>>>> dfef03c8e (同步远程)
    }

    for key, value in name_differences.items():
        if (param := params.get(key, None)) is not None:
<<<<<<< HEAD
            # Copy the parameter to new name then delete it, to prevent Ollama warning of invalid option provided
            params[value] = params[key]
            del params[key]

    # See https://github.com/ollama/ollama/blob/main/docs/api.md#request-8
    mappings = {
        "temperature": float,
        "top_p": float,
        "seed": lambda x: x,
        "mirostat": int,
        "mirostat_eta": float,
        "mirostat_tau": float,
        "num_ctx": int,
        "num_batch": int,
        "num_keep": int,
        "num_predict": int,
        "repeat_last_n": int,
        "top_k": int,
        "min_p": float,
        "typical_p": float,
        "repeat_penalty": float,
        "presence_penalty": float,
        "frequency_penalty": float,
        "penalize_newline": bool,
        "stop": lambda x: [bytes(s, "utf-8").decode("unicode_escape") for s in x],
        "numa": bool,
        "num_gpu": int,
        "main_gpu": int,
        "low_vram": bool,
        "vocab_only": bool,
        "use_mmap": bool,
        "use_mlock": bool,
        "num_thread": int,
    }

    return apply_model_params_to_body(params, form_data, mappings)
=======
            form_data[value] = param

    return form_data
>>>>>>> dfef03c8e (同步远程)


def convert_messages_openai_to_ollama(messages: list[dict]) -> list[dict]:
    ollama_messages = []

    for message in messages:
        # Initialize the new message structure with the role
        new_message = {"role": message["role"]}

        content = message.get("content", [])
<<<<<<< HEAD
        tool_calls = message.get("tool_calls", None)
        tool_call_id = message.get("tool_call_id", None)
=======
>>>>>>> dfef03c8e (同步远程)

        # Check if the content is a string (just a simple message)
        if isinstance(content, str):
            # If the content is a string, it's pure text
            new_message["content"] = content
<<<<<<< HEAD

            # If message is a tool call, add the tool call id to the message
            if tool_call_id:
                new_message["tool_call_id"] = tool_call_id

        elif tool_calls:
            # If tool calls are present, add them to the message
            ollama_tool_calls = []
            for tool_call in tool_calls:
                ollama_tool_call = {
                    "index": tool_call.get("index", 0),
                    "id": tool_call.get("id", None),
                    "function": {
                        "name": tool_call.get("function", {}).get("name", ""),
                        "arguments": json.loads(
                            tool_call.get("function", {}).get("arguments", {})
                        ),
                    },
                }
                ollama_tool_calls.append(ollama_tool_call)
            new_message["tool_calls"] = ollama_tool_calls

            # Put the content to empty string (Ollama requires an empty string for tool calls)
            new_message["content"] = ""

=======
>>>>>>> dfef03c8e (同步远程)
        else:
            # Otherwise, assume the content is a list of dicts, e.g., text followed by an image URL
            content_text = ""
            images = []

            # Iterate through the list of content items
            for item in content:
                # Check if it's a text type
                if item.get("type") == "text":
                    content_text += item.get("text", "")

                # Check if it's an image URL type
                elif item.get("type") == "image_url":
                    img_url = item.get("image_url", {}).get("url", "")
                    if img_url:
                        # If the image url starts with data:, it's a base64 image and should be trimmed
                        if img_url.startswith("data:"):
                            img_url = img_url.split(",")[-1]
                        images.append(img_url)

            # Add content text (if any)
            if content_text:
                new_message["content"] = content_text.strip()

            # Add images (if any)
            if images:
                new_message["images"] = images

        # Append the new formatted message to the result
        ollama_messages.append(new_message)

    return ollama_messages


def convert_payload_openai_to_ollama(openai_payload: dict) -> dict:
    """
    Converts a payload formatted for OpenAI's API to be compatible with Ollama's API endpoint for chat completions.

    Args:
        openai_payload (dict): The payload originally designed for OpenAI API usage.

    Returns:
        dict: A modified payload compatible with the Ollama API.
    """
    ollama_payload = {}

    # Mapping basic model and message details
    ollama_payload["model"] = openai_payload.get("model")
    ollama_payload["messages"] = convert_messages_openai_to_ollama(
        openai_payload.get("messages")
    )
    ollama_payload["stream"] = openai_payload.get("stream", False)

<<<<<<< HEAD
    if "tools" in openai_payload:
        ollama_payload["tools"] = openai_payload["tools"]

=======
>>>>>>> dfef03c8e (同步远程)
    if "format" in openai_payload:
        ollama_payload["format"] = openai_payload["format"]

    # If there are advanced parameters in the payload, format them in Ollama's options field
<<<<<<< HEAD
    if openai_payload.get("options"):
        ollama_payload["options"] = openai_payload["options"]
        ollama_options = openai_payload["options"]

        # Re-Mapping OpenAI's `max_tokens` -> Ollama's `num_predict`
        if "max_tokens" in ollama_options:
            ollama_options["num_predict"] = ollama_options["max_tokens"]
            del ollama_options[
                "max_tokens"
            ]  # To prevent Ollama warning of invalid option provided

        # Ollama lacks a "system" prompt option. It has to be provided as a direct parameter, so we copy it down.
        if "system" in ollama_options:
            ollama_payload["system"] = ollama_options["system"]
            del ollama_options[
                "system"
            ]  # To prevent Ollama warning of invalid option provided

    if "metadata" in openai_payload:
        ollama_payload["metadata"] = openai_payload["metadata"]
=======
    ollama_options = {}

    # Handle parameters which map directly
    for param in ["temperature", "top_p", "seed"]:
        if param in openai_payload:
            ollama_options[param] = openai_payload[param]

    # Mapping OpenAI's `max_tokens` -> Ollama's `num_predict`
    if "max_completion_tokens" in openai_payload:
        ollama_options["num_predict"] = openai_payload["max_completion_tokens"]
    elif "max_tokens" in openai_payload:
        ollama_options["num_predict"] = openai_payload["max_tokens"]

    # Handle frequency / presence_penalty, which needs renaming and checking
    if "frequency_penalty" in openai_payload:
        ollama_options["repeat_penalty"] = openai_payload["frequency_penalty"]

    if "presence_penalty" in openai_payload and "penalty" not in ollama_options:
        # We are assuming presence penalty uses a similar concept in Ollama, which needs custom handling if exists.
        ollama_options["new_topic_penalty"] = openai_payload["presence_penalty"]

    # Add options to payload if any have been set
    if ollama_options:
        ollama_payload["options"] = ollama_options
>>>>>>> dfef03c8e (同步远程)

    return ollama_payload
