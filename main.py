import sys
from pydoc import doc
from random import random
from newspaper import Article
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from pyinflect import getAllInflections
import re
from spacy.symbols import VERB
from pdfhelper import PDF
import wikipedia

from word_type import WordType

def get_wiki(str=None):
    wikipedia.set_lang('en')
    try:
        if str is None:
            log("Load wiki randomly")
            str = wikipedia.random(1)

        # load by text
        log("Load wiki by tile matching")
        page = wikipedia.page(str, None, True, True)
        content = page.content
    except:
        print("An exception occurred")    
        content = ""    
    
    return content


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    print("Got the content")
    return article.text

def log(str):
    print(str)

def generatePDF(file_name, contents):
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.watermark('fb.com/tailieutienganh', font_style='BI')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.add_font('DejaVuSans', fname='font/DejaVuSansCondensed.ttf')
    pdf.set_font('DejaVuSans', size=14)
    # File system title
    pdf.set_title(file_name)
    pdf.build_body(contents)
    pdf.output(str(file_name) + '.pdf', 'F')

def buildContents(text, kind):
    contents = []
    nlp = spacy.load('en_core_web_sm')
    text = re.sub('\n', '', text)
    doc = nlp(text)
    # Split to sentences
    sentence_tokens = [sent for sent in doc.sents]
    # Loop the sentence list
    for sent in sentence_tokens:

        print('interate a sent')
        # Tokenlize the sentence
        question = []
        notDone = True
        answer = []
        log('loop the array')
        for token in sent:
            if notDone and token.pos_ == kind:
                notDone = False
                question.append("______")

                # for the answer
                # get the base form
                lema = token.lemma_.lower()
                allInflections = getAllInflections(lema, pos_type='V')
                if allInflections is None:
                    continue
                answer = [inflect[0] for inflect in allInflections.values()]
                answer = list(dict.fromkeys(answer))
            else:
                question.append(token.text)

        contents.append((" ".join(question), answer))
    log('Shuffle the array')    
    np.random.shuffle(contents)
    log('Return the result')
    return contents

# contentss = buildContents("""I live in a house near the mountains. I have two brothers and one sister, and I was born last. My father teaches mathematics, and my mother is a nurse at a big hospital. My brothers are very smart and work hard in school. My sister is a nervous girl, but she is very kind. My grandmother also lives with us. She came from Italy when I was two years old. She has grown old, but she is still very strong. She cooks the best food!

# My family is very important to me. We do lots of things together do lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethedo lots of things togethe. My brothers and I like to go on long walks in the mountains. My sister likes to cook with my grandmother. On the weekends we all play board games together. We laugh and always have a good time. I love my family very much.""", VERB)
# article_content = get_article("https://en.wikipedia.org/wiki/2007_AT%26T_250")

def generateByType(file_name, type):
    wiki_content = get_wiki()
    if wiki_content == "":
        return
    built_content = buildContents(wiki_content, type)
    if len(built_content) < 10:
        return
    generatePDF("tlht_"+ str(type) + "_" + str(file_name), built_content)

def massGen(type, times):
    log("Mass gen")
    for i in range(int( times)):
        log("gen for" + str(i))
        generateByType(i, type)


if __name__ == '__main__':
    type = sys.argv[1]
    times = sys.argv[2]
    log("!!!!!!!Running with type " + type + " in " + str(times) + " times")

    massGen(type, times)
