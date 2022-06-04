from urllib import request
from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

query = "Where to find Pikachu"
googlefilter = 'site:https://pixelmonmod.com/wiki'

url = ""
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Referer': 'https://cssspritegenerator.com',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

for i in search(query+' '+googlefilter, num=1, stop=1):
    url = i
print(url)

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for data in soup(['table', 'script', 'style', 'comment']):
        data.decompose()
    bodycontent = soup.findAll('div', class_="mw-parser-output")
    visible_texts = filter(element_whitelist, bodycontent[0].findAll(text=True))
    return u" ".join(t.strip() for t in visible_texts) #[0:1024]

def element_whitelist(element):
    if element.parent.name in ['p','a']:
        return True
    return False

request = urllib.request.Request(url, data=None, headers=headers)
with urllib.request.urlopen(request) as response:
    html = response.read()
    context = text_from_html(html)
    print(context + ". \n" + "Check out: " + url)

