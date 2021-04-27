# -*- coding: utf-8 -*-
# pip install spacy ; pip install google ; pip install BeautifulSoup
# python -m spacy download en_core_web_sm

''' Import modules/libraries '''
import nltk
import spacy
import requests
import collections
import pandas as pd
import content_checker
from content_checker import extract_url, refine_text

from bs4 import BeautifulSoup
from googlesearch import search as gsearch
from countryinfo import CountryInfo
from spacy import displacy
# from textblob import TextBlob


''' Returns a string list of URLs based on a given search query '''
def getQueryResults(query, tld="com", lang="en", num_results=1, pause=2):
    query_results = []
    for url in gsearch(query, tld=tld, lang=lang, num=num_results, stop=num_results, pause=pause):
        query_results.append(url)
        print(url)

    print()
    return query_results

''' Returns list of collected content from URLs that are saved in queryResults'''
def extractWebData(query_results):
    extracted_data = []
    
    for result in query_results:
        res = requests.get(result, timeout=5)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        raw_text = soup.get_text(strip=True)
        content = extract_url(raw_text)
        clean_text = refine_text(content)
        extracted_data.append(clean_text)

    return extracted_data

## with spacy

''' Converts extracted web data into a processed SpaCy Doc object '''
def preprocessRawText(extracted_data):
    nlp = spacy.load("en_core_web_sm")

    for data in extracted_data:
        # content = unicode string object containing text data;  
        # doc = SpaCy model container containing sequence of token objects
        content = content_checker.refine_text(data)
        doc = nlp(content) 
        
        # accesses token attributes
        #tokens = [token.text for token in doc]
        #print(tokens)
        
        # lemmatises dataset as well as removing unmeaningful irrelevant words
        spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
        stopwords = [stopword for stopword in list(spacy_stopwords)] 
        refinedWords = [token for token in doc if not token.is_stop]
        lemmatisedWords = [(token, token.lemma_) for token in doc]
        
        # extracts the 5 most frequently occurred word
        wordFreq = collections.Counter(refinedWords)
        recurrentWords = wordFreq.most_common(5)
        uniqueWords = [word for (word, freq) in wordFreq.items() if freq == 1]
        
        # coarse-grained, fine-grained POS tags 
        taggedPOS = [(token, token.tag_, 
                        token.pos, spacy.explain(token.tag)) for token in doc]
        
        print(doc)
        tokenised_words = doc
        return tokenised_words

''' Returns a list of words with categorised NEs labelled '''
def locate_named_entities(tokenised_words):

    named_entities = []

    for ent in tokenised_words.ents:
        named_entities.append([ent.text, ent.label_])
    
    return named_entities

## with nltk
#def preprocess(extracted_data):
#    for data in extracted_data:
#        meep = idekanymore.make_right(data)
#        token = nltk.word_tokenize(meep)
#        stopwords = set(nltk.corpus.stopwords.words("english"))
#        refined_words = [ word for word in token if word not in stopwords ]
#        tagged_pos = nltk.pos_tag(refined_words)
#        entity = nltk.tree2conlltags(nltk.ne_chunk(tagged_pos))
#        print(nltk.conlltags2tree(entity))
#        
#    return "blah"


# def assignTokenTaggings(refinedWords):
#   return named_entities





# def recognise(entities):
#     named_entities = []
#     for chunk in entities:
#         current_chunk = " ".join([token for token, tagged_pos in chunk.leaves()])
#         if current_chunk not in named_entities:
#             named_entities.append(current_chunk)

    #print(f"Recognition of Named Entities (NER) with length {len(named_entities)}:\n\n{named_entities}")
