# -*- coding: utf-8 -*-

''' QueryExtractor.py '''
''' Webscraps data from multiple URLs, forms a manually created dataset '''

# Import libraries
import os, math
import requests, json
import numpy as np
import pandas as pd
import nltk, matplotlib, wikipedia, ety

# Specific modules being imported
from pprint import pprint
from collections import Counter
from googlesearch import search as gsearch
from bs4 import BeautifulSoup, SoupStrainer

from nltk import pos_tag, ne_chunk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tree import Tree
from nltk.chunk import conlltags2tree
from nltk.tag import StanfordNERTagger
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.ndimage import gaussian_gradient_magnitude
import matplotlib.pyplot as plt
from matplotlib import ticker
from PIL import Image

''' Global Variables '''
APP_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'img')                  # sets nested "img" folder path
INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics')     # creates folder named "infographics"

''' StanfordTagger = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                                    'stanford-ner-2018-10-16/stanford-ner.jar',
                                    encoding='utf-8') '''

class QueryExtractor():

    # class constructor
    def __init__ (self):
        self.query_results = []
        self.clean_html = []
        self.raw_text = ""
        self.splitsentence = ""
        
        self.tokens = []
        self.normalisedTokens = []  
        self.lowercasedTokens = []
        self.refinedTokens = []
        self.processedTokens = []

        self.wordsStemmed = []
        self.wordsLemmatised = []

        self.tagged_pos = [] 
        self.tagged_iob = [] 
        self.entities = []
        self.ne_freq_dict = {}
        self.top_frequent_entities = []
        
        self.merged_wikitext_dict = {
            'Entities': [], 'Frequencies': [], 'Wikitext': [], 'Etymologies': []
        }

        self.entities_dataframe = pd.DataFrame(
            columns = ['Entities', 'Frequencies', 'Wikitext', 'EtyWord', 'EtyLang'])
    
    ''' getQueryResults returns a list of URLs based on a given query ''' 
    def get_query_results(self, query):

        # retrieve the first 10 results from the 'gsearch' execution
        for link in gsearch(query, tld="com", lang="en", num=0, stop=3, pause=2):
            
            # for each iteration a link gets appended to a class member list, queryResults
            self.query_results.append(link)
            print(link) 

        return self.query_results

    ''' extractWebData returns list of collected content from URLs that are saved in queryResults '''
    def extract_webdata(self):
        results = self.query_results
        contentsList = self.clean_html
        
        linkCounter = 0
        for link in results:
            response = requests.get(link)                       # makes a HTTP request to the web server
            response.encoding  = response.apparent_encoding     # overrides existing encoding
            html_doc = response.text                            # collects the text content of the response object
            
            # parse the response data into structured format ---> HTML encoding gets converted from UTF-8 to Unicode 
            soup = BeautifulSoup(html_doc, "html.parser") # prettifiedSoup = soup.prettify()

            
            # strips out the content from the body of the HTML page
            cleanText = soup.get_text(strip=True)
            print(">>> HTML body text content have been retrieved ! | link #: ", linkCounter)
            linkCounter = linkCounter + 1

            contentsList.append(cleanText) 
            
            self.raw_text = ''.join(contentsList) 

        # list of stored text gets returned
        return self.raw_text


    ''' Preprocesses "raw_text" string data into a) splitted sentences; b) tokenised words ; c) annotated POS tags d) then returns a list of NEs '''
    def preprocess_textdata(self):
        self.splitsentence = sent_tokenize(self.raw_text)
        print(">>> 1) Splitting Sentences........ Raw data have been split into separate sentences !! \n")

        self.tokens = word_tokenize(self.raw_text)
        print(">>> 2) Tokenising Text............  Sentences have been tokenised into individual tokens!! \n", self.tokens, "\n")

        self.normalisedTokens = [word for word in self.tokens if word.isalpha()]
        print(">>> 3) Normalising Tokens......... Eliminated Non-Alphabetic Characters !! \n")

        # converts the transformed text-tokens into lowercase
        self.lowercasedTokens = [w.lower() for w in self.normalisedTokens]
        print(">>> 4) Lowercasing Tokens........... Tokens have now been lowercased !! \n")
        
        self.processedTokens = self.lowercasedTokens
        
        # omits unimportant "stopwords"
        stopwordList = set(stopwords.words("english"))
        self.refinedWords = [word for word in self.processedTokens if word not in stopwordList]
        print(">>> 5) Removing Stopwords.......... Tokens have been filtered with an updated list of words !! \n")

        # self.wordsStemmed = [self.ps.stem(word) for word in self.refinedWords]
        
        # self.wordsLemmatised = [self.lemm.lemmatize(word) for word in self.refinedWords] 
        return self.refinedWords

    # def get_tokens(self):
        """Returns the list of separated tokens """
        # return self.tokens

    ''' Annotates POLD labels to each separated tokens '''
    def classify_tokens(self):    
        self.tagged_pos = pos_tag(self.refinedWords) 
        print("\n>>> ", (type(self.tagged_pos), self.tagged_pos, "\n"))

        # classified_text = StanfordTagger.tag(self.refinedWords)
        self.entities = ne_chunk(self.tagged_pos, binary=True)
        print(type(self.entities))
        return self.entities
    
    ''' Counts up the frequency from a list of string named entities (indexed in the first position of each grouped tuple)'''
    def count_entities_frequency(self):
        self.ne_freq_dict = Counter(i[0] for i in self.entities)
        # pprint(self.ne_freq_dict)
        return self.ne_freq_dict


    """ def get_parts_of_speech_tag(self):
        return self.tagged_pos

    def process_iob_tags(self):
        tagged_prev = "0"
        tagged_ne = self.get_named_entity()

        for token, tag in tagged_ne:
            if tag == "O":
                self.tagged_iob.append((token, tag)) 
                tagged_prev = tag
                continue
            if tag != "O" and tagged_prev == "O":
                # NE begin
                self.tagged_iob.append((token, "B-"+tag))
                tagged_prev = tag

            elif tagged_prev != "O" and tagged_prev == tag:
                self.tagged_iob.append((token, "I-"+tag))
                tagged_prev = tag
            
            elif tagged_prev != "0" and tagged_prev != tag:
                self.tagged_iob.append((token, "B-"+tag)) 
                tagged_prev = tag
            
            return self.tagged_iob
        
     def get_tagged_iob(self):
            return self.tagged_iob
        
    def set_tree(self):
            tagged_pos = self.get_parts_of_speech_tag()
            tagged_iob = self.get_tagged_iob()

            tokens, ne_tags = zip(*tagged_iob)
            tagged_pos = [pos for token, pos in tagged_pos(tokens)]

            conlltags = [(tokens, pos, ne) for token, pos, ne in zip(tokens, tagged_pos, ne_tags)]
            ne_tree = conlltags2tree(colltags)
            return ne_tree
        
    def structure_named_entity(self):
            ne = []
            neo = []

            for subtree in ne_tree:

    
                def structure_named_entity(ne_tree):
					ne = []
					neo = []
					for subtree in ne_tree:
                        # If subtree is a noun chunk, i.e. NE != "O"
						if type(subtree) == Tree: 
							ne_label = subtree.label()
							ne_string = " ".join([token for token, pos in subtree.leaves()])
							ne.append((ne_string, ne_label))
						else:
							neo.append((subtree[0], "O"))
							if subtree[1] in ["VBD","VBG","VBN","VBP","VBZ"]:
								output["VERBS"].append(subtree[0]) """

                
    
    # DOESN'T WORK !
    ''' NER: returns a list of recognised Named Entities (NEs) through each POS tagged tokens '''
    # def recognise_named_entities(self):
    #     chunked_entities = ne_chunk(self.tagged_pos)
    #     current_chunk = []
        
    #     for chunk in chunked_entities:
    #         # print("Chunk", chunk)
    #         # if the selected chunk is of type "Tree", append the element from its leave to the current_chunk list
    #         # if type(chunk) == Tree:
    #         print("Type(chunk)", type(chunk))
    #         current_chunk.append(" ".join([token for token, taggedpos in chunk.leaves()]) )

    #         if current_chunk: 
    #             # print("Current chunk: ", current_chunk)
    #             entity = " ".join(current_chunk)
                
    #             if entity not in self.named_entities:
    #                 print("Entity", entity)
    #                 self.named_entities.append(entity)
    #                 current_chunk = []
    #         else:
    #             continue

    #     print(">>> Recognition Of Named Entities (NER) with length ", len(self.named_entities), "\n{}".format(self.named_entities))
    #     return (self.named_entities)

    """ def recogniseNamedEntities(self):
        for chunk in self.entities:
            currentChunk = " ".join(token for token, taggedpos in chunk.leaves())
            if currentChunk not in self.named_entities:
                self.named_entities.append(currentChunk)

            print(f'\n>>> Named Entity Recognition (NER) with length {len(self.named_entities)}: \n{self.named_entities}\n\n') """

  
    
    ''' Obtains the highest entity from the dict using its max value '''
    def get_frequent_entity(self):
        frequent_entiity = max(self.ne_freq_dict, key=self.ne_freq_dict.get)
        return frequent_entiity

    """  def get_multiple_frequent_entities(self):
        frequent_entities = []
        for _ in range(6):
            item = max(self.ne_freq_dict, key=self.ne_freq_dict.get)     
            self.ne_freq_dict.pop(item)
            frequent_entities.append(item)

        c = Counter(self.ne_freq_dict.values()) """
        
    def get_top_frequent_elements(self):
        self.top_frequent_entities = sorted(self.ne_freq_dict.items(), key=lambda t: t[1], reverse=True)[:6]
        return (self.top_frequent_entities)