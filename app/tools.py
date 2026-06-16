import requests

def joke_tool() -> str:
    res = requests.get("https://api.adviceslip.com/advice")
    data = res.json()
    return f"ADVICE: {data['slip']['advice']}"