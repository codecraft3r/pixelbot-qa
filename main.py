from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
import discord
import os
from dotenv import load_dotenv
from transformers import pipeline

#Global Variables
googlefilter = 'site:https://pixelmonmod.com/wiki'

model_name = "deepset/tinyroberta-squad2"

qa_model = pipeline("question-answering", model=model_name,tokenizer=model_name)

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://cssspritegenerator.com',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

#webscraping
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    for data in soup(['table', 'script', 'style', 'comment']):
        data.decompose()
    bodycontent = soup.findAll('div', class_="mw-parser-output")
    visible_texts = filter(
        element_whitelist, bodycontent[0].findAll(text=True))
    return u" ".join(t.strip() for t in visible_texts)  # [0:1024]


def element_whitelist(element):
    if element.parent.name in ['p', 'a']:
        return True
    return False

#AI stuff
def get_answer(question,context):
    return qa_model(question, context)["answer"]

#.env stuff
load_dotenv()
#Discord
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    activity = discord.Activity(type=discord.ActivityType.listening, name="!wiki")
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    if(message.content.startswith('!wiki')):
        await message.reply("*Searching...*", mention_author=False)
        for i in search(message.content[6:] + ' ' + googlefilter, num=1, stop=1):
            url = i
        request = urllib.request.Request(url, data=None, headers=headers)
        with urllib.request.urlopen(request) as response:
            html = response.read()
        text = text_from_html(html)
        ans = get_answer(message.content[6:],text)
        await message.reply(+ ans + ". \n*From source:* " + url)

client.run(os.getenv('DISCORD_TOKEN'))
