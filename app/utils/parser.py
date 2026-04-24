import json
import re


def _clean_and_parse(result):
    content = result.get("response") or result
    if isinstance(content, dict):
        return content
    # hapus ```json ... ```
    content = re.sub(r"```json\n?|\n?```", "", content).strip()
    return json.loads(content)


def parse_tree_response(result):
    try:
        return _clean_and_parse(result)
    except Exception as e:
        raise Exception(f"Invalid JSON from LLM (generate): {str(e)}")


def parse_identify_response(result):
    try:
        return _clean_and_parse(result)
    except Exception as e:
        raise Exception(f"Invalid JSON from LLM (identify): {str(e)}")
