from bs4 import BeautifulSoup

def extract_text_from_html(html_content):

    if not html_content or not isinstance(html_content, str):
        return {"regular": "", "important": ""}

    soup = BeautifulSoup(html_content, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    for hidden in soup.find_all(True, style=True):
        style = hidden["style"].lower()
        if "display:none" in style or "visibility:hidden" in style or "opacity:0" in style:
            hidden.extract()

    for hidden in soup.find_all(class_=["hidden", "invisible", "offscreen", "screen-reader"]):
        hidden.extract()

    for hidden in soup.find_all(attrs={"aria-hidden": "true"}):
        hidden.extract()

    for footer in soup.find_all("footer"):
        footer.extract()

    important_text = []
    for tag in soup.find_all(["title", "h1", "h2", "h3", "b", "strong"]):
        if tag.get_text(strip=True):
            important_text.append(tag.get_text(strip=True))

    clean_text = soup.get_text(separator=" ", strip=True)

    clean_text = " ".join(clean_text.split())

    return {
        "regular": clean_text,
        "important": " ".join(important_text)
    }