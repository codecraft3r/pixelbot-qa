from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request
import discord
import os
from dotenv import load_dotenv
from transformers import pipeline

# Global Variables
googlefilter = 'site:https://pixelmonmod.com/wiki' # site filter for google search

model_name = "deepset/tinyroberta-squad2" # question answering model name from https://huggingface.co/models

qa_model = pipeline("question-answering", model=model_name,tokenizer=model_name) # load the model

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Referer': 'https://cssspritegenerator.com',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'} # fake a user agent, since mediawiki doesn't like scrapers

# Webscraping
def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser') # create a new bs4 object from the html data loaded
    for data in soup(['table', 'script', 'style', 'comment']): # remove all the tables, scripts, styles, and comments
        data.decompose()
    bodycontent = soup.findAll('div', class_="mw-parser-output") # grab the div that contains the wiki text
    useful_texts = filter(element_isUseful, bodycontent[0].findAll(text=True)) # filter out any tags that aren't useful
    return u" ".join(t.strip() for t in useful_texts) # return a string of all the useful text


def element_isUseful(element):
    if element.parent.name in ['p', 'a']:
        return True
    return False

# AI stuff
def get_answer(question,context):
    return qa_model(question, context)["answer"]

# .env stuff
load_dotenv() 
# Discord
client = discord.Client()


@client.event
async def on_ready():
    # inform user of bot status
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # set bot status to "listening to !wiki"
    activity = discord.Activity(type=discord.ActivityType.listening, name="!wiki")
    await client.change_presence(activity=activity)


@client.event
async def on_message(message):
    # !wiki command
    if(message.content.startswith('!wiki')):
        await message.reply("*Searching...*", mention_author=False) # inform user that their request is being processed
        for i in search(message.content[6:] + ' ' + googlefilter, num=1, stop=1): # search google for the query with googlefilter
            url = i # get url from google search
        request = urllib.request.Request(url, data=None, headers=headers) # create request
        with urllib.request.urlopen(request) as response: # open request
            html = response.read() # read response (website data)
        context = text_from_html(html) # get text from website
        ans = get_answer(message.content[6:],context) # get answer from AI using website data as context
        await message.reply(ans + ". \n*From source:* " + url) # reply with answer and url

client.run(os.getenv('DISCORD_TOKEN'))
