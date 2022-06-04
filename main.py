from urllib import request
from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

query = "How to catch pokemon site:https://pixelmonmod.com/wiki"
url = ""
for i in search(query, num=1, stop=1):
    url = i

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
  
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

html = urllib.request.urlopen(url)
print(text_from_html(html))
