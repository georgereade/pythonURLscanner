import requests
from bs4 import BeautifulSoup
import string
import re

# Making a request to get HTML from a page
url = "https://www.bbc.co.uk/news/uk-67087757"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}
r = requests.get(url, headers=headers)
print(f"Response Code: {r.status_code}")
print(f"Response Code: {r.reason}")


# Converting the HTML into a structured object
html = r.text
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in html.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
html = '\n'.join(chunk for chunk in chunks if chunk)
soup = BeautifulSoup(html, "html.parser")
with open("webpage.html", "w", encoding="utf-8") as f:
    f.write(str(soup))


# Identify p elements and return text
input_folder = "input/article-text.txt"
paragraphs = soup.find_all("p")
h1 = soup.find_all("h1")
h2 = soup.find_all("h2")

df = open(input_folder, "w", encoding="utf-8")

for p in paragraphs:
    ptext = p.get_text()
    df.write(ptext + ' ')

for i in h1:
    h1text = i.get_text()
    df.write(h1text + ' ')

for i in h2:
    h2text = i.get_text()
    df.write(h2text + ' ')

df.close()


# opening and creating new .txt file
with open(
    "input/article-text.txt", 'r', encoding="utf-8") as r, open(
        "input/article-text-clean.txt", 'w', encoding="utf-8") as o:

    for line in r:
        # isspace() function
        if not line.isspace():
            o.write(line)


def text_search(keyword: str, text_to_search: str) -> int:
    """
    Count the number times the keyword appears in the text
    """
    translator = str.maketrans(
        string.punctuation, ' ' * len(string.punctuation))
    try:
        text = text_to_search.translate(translator).lower()
    except Exception as e:
        text = ""
        print(f"Error: {e}")
    occurrences = text.count(keyword.lower())
    return occurrences


def first_sentences(keyword: str, text_to_search: str) -> str:
    try:
        text = text_to_search.lower()
        returned_text = ['\n']
        count = 0
        sentences = text.split('. ')
        # sentences = re.split('. | ? ', text)
        for sentence in sentences:
            if count >= 2:
                break
            if keyword in sentence:
                returned_text.append(sentence.strip() + '. \n\n')
                count += 1
        return ''.join(returned_text)
    except Exception as e:
        text = ""
        print(f"Error: {e}")

    return None


sample_text_file = "input/article-text-clean.txt"
with open(sample_text_file, "r", encoding="utf-8") as f:
    sample_text = f.read()

sample_keyword = input("Enter search term: ").lower()

word_count = text_search(keyword=sample_keyword, text_to_search=sample_text)
first_sentence = first_sentences(
    keyword=sample_keyword, text_to_search=sample_text)
occurrences_sentence = f"Found {word_count} occurrences in the text"
print(occurrences_sentence)
print(first_sentence)

save_file_location = "output/save_string.txt"
with open(save_file_location, "w") as f:
    f.write(occurrences_sentence)
