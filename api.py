import requests

API_KEY = ""
URL = "https://api-free.deepl.com/v2/translate"

def get_alternative_translations(word, source_lang="EN", target_lang="UK"):
    params = {
        "auth_key": API_KEY,
        "text": word,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "tag_handling": "xml",
        "split_sentences": 0,
        "preserve_formatting": 1
    }
    
    response = requests.post(URL, data=params)
    if response.status_code == 200:
        translated_text = response.json()["translations"][0]["text"]
        return translated_text
    else:
        return f"Error: {response.status_code} - {response.text}"

word = "ecclesiastical"
translation = get_alternative_translations(word)
print(f"Translation of {word}: {translation}")
