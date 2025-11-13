# function_app.py
import json
import logging
import azure.functions as func
import sys

app = func.FunctionApp()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


def _extract_arguments(context: str, tool_name: str) -> dict:
    try:
        payload = json.loads(context)
        args = payload.get("arguments", {})
        logger.info("%s invoked", tool_name)
        logger.debug("%s payload: %s", tool_name, payload)
        return args
    except Exception:
        logger.exception("Failed to parse context for %s", tool_name)
        return {}

# ツール: テキストを反転する
tool_properties_reverse_json = json.dumps([
    {
        "propertyName": "text",
        "propertyType": "string",
        "description": "text to reverse"
    }
])

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="reverse_text",
    description="Return the reversed string of the provided text.",
    toolProperties=tool_properties_reverse_json
)
def reverse_text(context) -> str:
    """
    MCPの argumentsから textを受け取り、反転して返す。
    """
    """
    Example context:
    {
        "toolName": "reverse_text",
        "arguments": {
            "text": "example"
        },
        "toolCallId": "xxx",
        "invocationId": "xxx"
    }
    """
    args = _extract_arguments(context, "reverse_text")
    text = args.get("text")

    if not text:
        logger.warning("reverse_text received no text argument")
        return "No text provided."
    if not isinstance(text, str):
        logger.info("reverse_text converting non-string input of type %s", type(text).__name__)
        text = str(text)
    result = text[::-1]
    logger.info("reverse_text succeeded")
    logger.debug("reverse_text result: %s", result)
    return result

# ツール: テキストを大文字に変換する
tool_properties_upper_json = json.dumps([
    {
        "propertyName": "text",
        "propertyType": "string",
        "description": "Uppercase this text."
    }
])

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="to_upper",
    description="Uppercase a given text.",
    toolProperties=tool_properties_upper_json
)
def to_upper(context) -> str:
    args = _extract_arguments(context, "to_upper")
    text = args.get("text", "")
    result = text.upper()
    logger.info("to_upper succeeded")
    logger.debug("to_upper result: %s", result)
    return result


# ツール: テキストを小文字に変換する
tool_properties_lower_json = json.dumps([
    {
        "propertyName": "text",
        "propertyType": "string",
        "description": "Lowercase this text."
    }
]) 

@app.generic_trigger(
    arg_name="context",
    type="mcpToolTrigger",
    toolName="to_lower",
    description="Lowercase a given text.",
    toolProperties=tool_properties_lower_json
)
def to_lower(context) -> str:
    args = _extract_arguments(context, "to_lower")
    text = args.get("text", "")
    result = text.lower()
    logger.info("to_lower succeeded")
    logger.debug("to_lower result: %s", result)
    return result