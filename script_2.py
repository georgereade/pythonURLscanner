import requests
from bs4 import BeautifulSoup
import string

# Making a request to get HTML from a page
url = "https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population"
r = requests.get(url)
print(f"Response Code: {r.status_code}")

# Converting the HTML into a structured object
html = r.text
soup = BeautifulSoup(html, "html.parser")
with open("test.html", "w", encoding="utf-8") as f:
    f.write(str(soup))

# Identify p elements and return text
input_folder = "input/article-text.txt"
paragraphs = soup.find_all("p")
h1 = soup.find_all("h1")
h2 = soup.find_all("h2")

df = open(input_folder, "w", encoding="utf-8")

for i in h1:
    h1text = i.get_text()
    df.write(h1text)

for i in h2:
    h2text = i.get_text()
    df.write(h2text)

for p in paragraphs:
    ptext = p.get_text()
    df.write(ptext)

df.close()


def text_search(keyword: str, text_to_search: str) -> int:
    """
    Count the number times the keyword appears in the text
    """
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    try:
        text = text_to_search.translate(translator).lower()
    except Exception as e:
        text = ""
        print(f"Error: {e}")
    occurrences = text.count(keyword.lower())
    return occurrences


sample_text_file = "input/article-text.txt"
with open(sample_text_file, "r") as f:
    sample_text = f.read()

sample_keyword = "states"

word_count = text_search(keyword=sample_keyword, text_to_search=sample_text)
occurrences_sentence = f"Found {word_count} occurrences in the text"
print(occurrences_sentence)

save_file_location = "output/save_string.txt"
with open(save_file_location, "w") as f:
    f.write(occurrences_sentence)