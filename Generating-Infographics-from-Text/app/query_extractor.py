#------------------------------------------------------------------------------------------------
#-- GIFT Apps query_extractor.py
#------------------------------------------------------------------------------------------------

#!/usr/bin/Python
# -*- coding: utf-8 -*-

# Import libraries
import os
import requests, json
import numpy as np
import nltk, matplotlib

# Specific modules being imported
from flask import url_for
from pprint import pprint
from collections import Counter
from googlesearch import search as gsearch
from bs4 import BeautifulSoup, SoupStrainer
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.ndimage import gaussian_gradient_magnitude
from matplotlib import pyplot as plt
from PIL import Image

''' Global Variables '''
# WORDCLOUD_DIR = os.path.join('../static/img', 'infographics')
# INFOGRAPHICS_DIR = os.path.abspath('/static/img/infographics/')

APP_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'img')                  # sets nested "img" folder path
INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics')     # creates folder named "infographics"

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

        self.taggedpos = []  
        self.entities = []
        self.ne_freq_dict = {}
        self.top_frequent_entities = []
        self.merged_wikitext_dict = {
            'Entities': [],
            'Frequencies': [],
            'Wikitext': []
        }
    
    ''' getQueryResults returns a list of URLs based on a given query ''' 
    def get_query_results(self, query):

        # retrieve the first 10 results from the 'gsearch' execution
        for link in gsearch(query, tld="com", lang="en", num=10, stop=10, pause=2):
            
            # for each iteration a link gets appended to a class member list, queryResults
            self.query_results.append(link)
            print(link) 

        return self.query_results

    ''' extractWebData returns list of collected content from URLs that are saved in queryResults '''
    def extract_webdata(self):
        results = self.query_results
        contentsList = self.clean_html
    
        for link in results:
            linkCounter = 1
            response = requests.get(link)                       # makes a HTTP request to the web server
            response.encoding  = response.apparent_encoding     # overrides existing encoding
            html_doc = response.text                            # collects the text content of the response object
            
            # parse the response data into structured format ---> HTML encoding gets converted from UTF-8 to Unicode 
            soup = BeautifulSoup(html_doc, "html.parser") # prettifiedSoup = soup.prettify()

            
            # strips out the content from the body of the HTML page
            cleanText = soup.get_text(strip=True)
            print(">>> HTML body text content have been retrieved ! | link #: ", linkCounter,"\n")
            linkCounter = linkCounter + 1

            contentsList.append(cleanText) 
            
            self.raw_text = ''.join(contentsList) 

        # list of stored text gets returned
        return self.raw_text


    ''' Preprocesses "raw_text" string data into a) splitted sentences; b) tokenised words ; c) annotated POS tags d) then returns a list of NEs '''
    def preprocess_textdata(self):
        self.splitsentence = sent_tokenize(self.raw_text)
        print(type(self.splitsentence))
        print(">>> 1) Splitting Sentences........ Raw data have been split into separate sentences !! \n")

        self.tokens = word_tokenize(self.raw_text)
        print(type(self.tokens))
        print(">>> 2) Tokenising Text............  Sentences have been tokenised into individual tokens!! \n", self.tokens, "\n")

        self.normalisedTokens = [word for word in self.tokens if word.isalpha()]
        print(type(self.normalisedTokens))
        print(">>> 3) Normalising Tokens......... Eliminated Non-Alphabetic Characters !! \n")

        # converts the transformed text-tokens into lowercase
        self.lowercasedTokens = [w.lower() for w in self.normalisedTokens]
        print(type(self.lowercasedTokens))
        print(">>> 4) Lowercasing Tokens........... Tokens have now been lowercased !! \n")
        
        self.processedTokens = self.lowercasedTokens
        print(type(self.processedTokens))
        
        stopwordList = set(stopwords.words("english"))
        self.refinedWords = [word for word in self.processedTokens if word not in stopwordList]
        print(type(self.refinedWords))
        print(">>> 5) Removing Stopwords.......... Tokens have been filtered with an updated list of words !! \n")

        # self.wordsStemmed = [self.ps.stem(word) for word in self.refinedWords]
        
        # self.wordsLemmatised = [self.lemm.lemmatize(word) for word in self.refinedWords] 
        
        self.taggedpos = pos_tag(self.refinedWords) 
        print(type(self.taggedpos))
        print("\n>>> ", self.taggedpos, "\n")

        self.entities = ne_chunk(self.taggedpos, binary=True)
        print(type(self.entities))
        return self.entities

    ''' Counts up the frequency from a list of string named entities (indexed in the first position of each grouped tuple) '''
    def count_entities_frequency(self):
        self.ne_freq_dict = Counter(i[0] for i in self.entities)
        # pprint(self.ne_freq_dict)
        return self.ne_freq_dict
    
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
        
    ''' Returns a long dictionary items with nested list of string entities, integer frequencies and string wikitext'''
    def merge_entity_wikitext(self):

        for i in self.top_frequent_entities:
            # content of entity, frequency, wikitext gets stored into each specified position in dict 
            # self.merged_wikitext_dict[i[0]] = wikipedia.summary((i), sentences=2)
            self.merged_wikitext_dict['Entities'].append(i[0])
            self.merged_wikitext_dict['Frequencies'].append(i[1])
            self.merged_wikitext_dict['Wikitext'].append(wikipedia.summary((i), sentences=2)
        
        return (self.merged_wikitext_dict)
    
    ''' Returns a Pandas dataframe generated from data stored in a dictionary '''
    def build_entities_dataframe(self):
        data = self.merged_wikitext_dict
        df = pd.DataFrame.from_dict(data, columns = ['Entities', 'Frequency', 'Wikitext'])
        return df 


    '''  Generates a visual figure, rendering that image as a wordcloud graphic which contains frequent tokens '''
    # def generate_wordcloud(self, imgWordCloud):
        # print("Frequent Entity {}".format(frequent_entiity))

    #   #alice_mask = np.array(Image.open(path.join(d, "1.png")))
        # stopwords = set(STOPWORDS)

        # generates an instantiated wordcloud object with defined properties set
        # wordcloud = WordCloud(width=1000, height=1000, max_words=1000, margin=10, background_color="white", random_state = 1)
        # wordcloud.generate_from_frequencies(self.ne_freq_dict)
            #mask=alice_mask

        # renders the generated wordcloud as a visual
        #     # plt.figure()
        #     #     # plt.imshow(wordcloud, interpolation = 'bilinear')       # display-image appears more smooth
        #     #     # plt.axis("off")                                         # removes x/y graph axis
        #     #     # plt.show()                                              # displays all figures
            
        #     #     # saves the generated plot figure as an image file in current directory
        #     #     # wordcloud.to_file(imgWordCloud)  
        
        # wordcloud.to_file(os.path.join(INFOGRAPHICS_DIR, imgWordCloud))
        # return wordcloud

    # #----------------------------------------------------------------------------------------------------------
    # #-- Generates a visual figure, rendering that image as a wordcloud graphic which contains frequent tokens
    # #----------------------------------------------------------------------------------------------------------    
    # def create_masked_wordcloud(self, imgWordCloud):
    #     bubbleimg = np.array(Image.open(os.path.join(INFOGRAPHICS_DIR, 'bubblemask.jpg')))

    #     # colour white is masked out from the bubble
    #     bubblemask = bubbleimg.copy()
    #     bubblemask[bubblemask.sum(axis=2) == 0] = 255

    #     # filtered array with the use of multidimentional gradient magnitude using Gaussian derivatives
    #     edges = np.mean([gaussian_gradient_magnitude(
    #                     bubblemask[:,:,i] / 255., 2) for i in range(3)], axis=0)
    #     bubblemask[edges > .08] = 255

    #     stopwords = set(STOPWORDS)
    #     # generates an instantiated wordcloud object with defined properties set
    #     wc = WordCloud(width=1000, height=1000, max_words=1000, margin=10, background_color="grey", 
    #                     random_state=1, stopwords=stopwords, mask=bubblemask)

    #     wc.generate_from_frequencies(self.ne_freq_dict)
    #     wc.to_file(os.path.join(INFOGRAPHICS_DIR, 'bubblemaskedwordcloud.jpg'))

    #     # creates colourised wordcloud from generated plot figure
    #     image_colours = ImageColorGenerator(bubbleimg)
    #     wc.recolor(color_func=image_colours)
    #     wc.to_file(os.path.join(INFOGRAPHICS_DIR, "bubblemaskedcolouredwordcloud.jpg"))

    #     return wc

    # def create_flag_masked_wordcloud(self, imgWordCloud):
    #     stopwords = set(STOPWORDS)
    #     flagimg = np.array(Image.open(os.path.join(INFOGRAPHICS_DIR, 'UK-flag.jpg')))
    #     wc = WordCloud(width=500, height=500, max_words=1000, margin=10, random_state=42, background_color="grey",
    #                     stopwords=stopwords, mask=flagimg)
    #     wc.generate_from_frequencies(self.ne_freq_dict)
    #     wc.to_file(os.path.join(INFOGRAPHICS_DIR, 'ukflagmaskedcolouredwordcloud.jpg'))
    #     return wc

    # def create_map_masked_wordcloud(self, imgWordCloud):
    #     return 0
#----------------------------------------------------------------------------------------------------------- 
# #-- Moves the image file located in a temporary directory to a destination folder 
#-----------------------------------------------------------------------------------------------------------
# def transfer_wordcloud_imagefile(self, imgWordCloud):
        
 #     temp_wordcloud_dir = os.path.join(STATIC_DIR, imgWordCloud)
    #     dest_wordcloud_dir = os.path.join(INFOGRAPHICS_DIR, imgWordCloud)
    #     updated_wordcloud_dir = os.replace(temp_wordcloud_dir, dest_wordcloud_dir)
#     return updated_wordcloud_dir


# only_p_tags = SoupStrainer("p")

# JSON is used to load each 'link' response into a dictionary 
# json_response_dict = json.loads(response.text)

# for i in json_response_dict:
#     print("Key: ", i, "val: ", json_response_dict[i])
# UnicodeDammit.detwingle(doc)
# 
# # {{ url_for('static', filename='img/title-logo.jpg')}} " 
# <img src="{{url_for('static/img/infographics', filename='word-cloud-pic.jpg')}}" width = 500 height 500/>