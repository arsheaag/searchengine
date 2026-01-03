import re
from nltk.stem import PorterStemmer

HTML_WORDS = {"b", "c", "i", "u", "script", "alert", "noscript", "div", "span", "meta", "style", "href"}

stemmer = PorterStemmer()

def tokenize(text: str) -> list[str]:
    if not text or not isinstance(text, str):
        return []

    text = text.lower()

    text = re.sub(r"\b(?:{})\b".format("|".join(HTML_WORDS)), "", text)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    tokens = text.split()

    stemmed_tokens = [stemmer.stem(word) for word in tokens]

    unique_tokens = list(dict.fromkeys(stemmed_tokens))

    return unique_tokens

def compute_word_frequencies(tokens: list[str]) -> dict[str, int]:
    token_dict = {}
    for word in tokens:
        token_dict[word] = token_dict.get(word, 0) + 1
    return token_dict