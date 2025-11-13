# function_app.py
import json
import azure.functions as func

app = func.FunctionApp()

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
    try:
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
        payload = json.loads(context)
        args = payload.get("arguments", {})
        text = args.get("text")
    except Exception:
        text = None

    if not text:
        return "No text provided."
    if not isinstance(text, str):
        text = str(text)
    return text[::-1]

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
    args = json.loads(context).get("arguments", {})
    text = args.get("text", "")
    return text.upper()


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
    args = json.loads(context).get("arguments", {})
    text = args.get("text", "")
    return text.lower()