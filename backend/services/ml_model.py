def smart_search(keyword: str):
    keyword = keyword.lower()

    result = {}

    if "หญิง" in keyword or "female" in keyword:
        result["type"] = "female"

    if "ชาย" in keyword or "male" in keyword:
        result["type"] = "male"

    if "sc3" in keyword:
        result["building"] = "SC3"

    return result


def predict_crowd():
    return "medium"