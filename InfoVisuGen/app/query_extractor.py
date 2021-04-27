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

""" StanfordTagger = StanfordNERTagger('stanford-ner-2018-10-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                                    'stanford-ner-2018-10-16/stanford-ner.jar',
                                    encoding='utf-8')  """

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
        for link in gsearch(query, tld="com", lang="en", num=10, stop=10, pause=2):
            
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

        classified_text = StanfordTagger.tag(self.refinedWords)
        self.entities = ne_chunk(self.tagged_pos, binary=True)
        print(type(self.entities))
        return self.entities
    
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
        
    # ''' Returns a long dictionary items with nested list of string entities, integer frequencies and string wikitext'''
    # def merge_entity_wikitext(self):

    #     for i in self.top_frequent_entities:
    #         # content of entity, frequency, wikitext gets stored into each specified position in dict 
    #         # self.merged_wikitext_dict[i[0]] = wikipedia.summary((i), sentences=2)
    #         self.merged_wikitext_dict['Entities'].append(i[0])
    #         self.merged_wikitext_dict['Frequencies'].append(i[1])
    #         self.merged_wikitext_dict['Wikitext'].append(wikipedia.summary((i[0]), sentences=2))
        
    #     return (self.merged_wikitext_dict)
    

    ''' TF-IDF measures frequency of word in document & the inverse importance of document frequency in whole set of corpus '''
    """  def computes_tfidf_graph(self):
        # t = term(word); d = document(set of words); n = count of corpus
        # corpus = total document set
        # tf = frequency counter for term T in document D
        # df = count of occurences of term T in document set N
        
        term_freq = 0             # number of times term T appears in document 
        total_terms_in_doc = 0    # total number of terms in document
        total_num_doc = 1
        inv_doc_freq = 0          # number of documents with term T in it 
        N = 0                      # total number of corpora

        tfidf = {}
        tokens = self.get_tokens()
        tokens_set = set(tokens)
        for word in tokens_set:
            tf = float(tokens.count(word)) / len(tokens_set)
            idf = math.log(float(1 + total_num_doc))                  
            tfidf[word] = tf * idf

        return sorted(tfidf.items(), key=itemgetter(1), reverse=True) """

    ''' Returns a long dictionary items with nested list of string entities, integer frequencies and string wikitext'''
    def merge_entities_wikitext(self):
        
        print(">>> Top Frequent Entities: ", self.top_frequent_entities)
        
        # content of entity, frequency, wikitext gets stored into each specified position in dict 
        # catches & handles the exception encountered in the try-clause
        for i in self.top_frequent_entities:
            try:  
                self.merged_wikitext_dict['Entities'].append(i[0])
                self.merged_wikitext_dict['Frequencies'].append(i[1])
                self.merged_wikitext_dict['Wikitext'].append(wikipedia.summary((i[0]), sentences=1))
            
            except wikipedia.exceptions.DisambiguationError as error:
                self.merged_wikitext_dict['Wikitext'].append(error.options[0])
        
        return self.merged_wikitext_dict

     # self.merged_wikitext_dict[i[0]] = wikipedia.summary((i), sentences=2)

    ''' Returns a Pandas dataframe generated from data stored in a dictionary '''
    # def build_entities_dataframe(self):
    #     data = self.merged_wikitext_dict
    #     self.entities_dataframe = pd.DataFrame.from_dict(data, columns = ['Entities', 'Frequency', 'Wikitext'])
    #     return (self.entities_dataframe) 

    ''' Returns a contructed dataframe consisting of entities, wikitext, and etymologies '''
    # def construct_etymology_merge(self):
    #     for row in range(len(self.entities_dataframe)) :
    #         # print(self.entities_dataframe.iloc[row, 0])
        
    #         # stores each row onto a new column
    #         # retrieves origins of each row indexed in the first "entities" column
    #         self.entities_dataframe.append( { 'Etymologies': ety.origins(self.entities_dataframe.iloc[row,0]) })
        
    #     return (self.entities_dataframe)

    ''' Returns a contructed Pandas dataframe consisting of entities, frequency, wikitext, and etymologies '''
    def construct_entities_dataframe(self):
        items = self.merged_wikitext_dict
        
        etymology_word = []
        etymology_lang = []
        
        for entity in self.merged_wikitext_dict['Entities']:
            try:
                origins = ety.origins(entity)
                origin = origins[0]
                originated_word = origin.word
                originated_lang = origin.language
                etymology_word.append(originated_word)
                etymology_lang.append(originated_lang)
            
            except IndexError:
                origins = entity
                originated_word = origins
                originated_lang = "English"
                etymology_word.append(originated_word)
                etymology_lang.append(originated_lang)

        # transfers specified dictionary items into the empty dataframe object
        for entities, frequencies, wikitext in zip(items['Entities'], items['Frequencies'], items['Wikitext']):
            self.entities_dataframe = self.entities_dataframe.append({ 
                                            'Entities': entities,
                                            'Frequencies': frequencies,
                                            'Wikitext': wikitext,
                                            'EtymologyWord': etymology_word,
                                            'EtymologyLang': etymology_lang}, ignore_index=True)
        # print(self.entities_dataframe.head())

        # for row in range(len(self.entities_dataframe)) :
        #     origins = ety.origins(self.entities_dataframe.iloc[row,0])
                        
        #     # check if length of a list is equal to zero 
        #     # if len(variable) == 0:
        #     if not origins :
        #         print("List is empty")

        #     if origins:
        #         print(type(origins))
        #         if (len(origins) > 0):
        #             # add data from variable to the dataframe
        #             origin = origins[0].word
        #         else:
        #             origin = 1

        #         # appends "origins" of each row's "entities" (indexed at '0') to a newly created column "Etymologies"
        #         self.entities_dataframe = self.entities_dataframe.append({'Etymologies' : origin}, ignore_index=True)
        #         df.
        
        print(self.entities_dataframe.head())
        return (self.entities_dataframe)  

    # self.entities_dataframe['Etymologies'][row] = ety.origins(self.entities_dataframe.iloc[row,0])



    '''  Generates a visual timeline figure, rendering that image from items contained in a dataframe '''
    """   def plot_timeline(self, tmpimg):
        # plot df values
        df = self.entities_dataframe
    
        # entities = self.ne_freq_dict.keys()
        #entities = df.iloc[:,0].astype('|S')                     # [col[0] for col in df.iloc]       # df.iloc[:,0]
        #print(type(entities))   
        #frequency = df.iloc[:,1].astype('|S')           # df['Frequencies']       # [col[1] for col in df.iloc]       # df.iloc[:,1]
        #wikitext = df.iloc[:,2]                         # df['Wikitext']           # [col[2] for col in df.iloc]       # df.iloc[:,2]
        #etymologies = df.iloc[:,3].astype('|S')      # df['Etymologies']     # [col[3] for col in df.iloc]       # df.iloc[:,3]
        
        items = self.merged_wikitext_dict
        print(items)

        entities = items['Entities']
        print("\n")
        print(items['Entities'])

        frequency = items['Frequencies']
        wikitext = items['Wikitext']
        etymologies = df.iloc[:,3].to_string()
        # creates stem plot with some variation in level to distinguish close-by events
        # for each event a text label via annotate is added (which is offset in units of points from the tip of the event line)
        
        # sets some levels intervals
        levels = np.tile([-5, 5, -3, 3, -1, 1],
                 int(np.ceil(len(entities)/6)))[:len(entities)]

        # generates figure with axis
        fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
        ax.set(title="Entities, Wikitext, Etymologies")
        
        print(type(levels))

        #Come back to this if dataplot is not working properly of format 
        # sets vertical stem and adds baseline, markerline to it
        ax.vlines(frequency, 0, levels, color="tab:red")
        ax.plot(frequency, np.zeros_like(frequency), "-o", color="k", markerfacecolor="w")
       

        for entity, level, freq in zip(entities, levels, frequency):
            ax.annotate(freq, xy=(entity,1), xytext=(-3, np.sign(1)*3), 
            textcoords="offset points", horizontalalignment="right", 
            verticalalignment="bottom" if level > 0 else "top")

        # formats x-axis of the stem plot
        #ax.get_xaxis().set_major_locator(entities)                      # DOESN'T WORK   
        
        # Fixed formatter
        # FixedFormatter should only be used together with FixedLocator.
        # Otherwise, one cannot be sure where the labels will end up.
        positions = [0, 1, 2, 3, 4, 5]
        labels = []
        for entity in entities:
            labels.append(entity)

        ax.xaxis.set_major_locator(ticker.FixedLocator(positions))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))

        
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")     # gets the tick labels as a list of Text instances and rotates them





        # removes y-axis and spimes
        ax.get_yaxis().set_visible(False)
        for spine in ["left", "top", "right"]:
            ax.spines[spine].set_visible(False)
        ax.margins(y=0.1)
        
        # saves the figure as an image file onto a specified directory
        plt.savefig(os.path.join(INFOGRAPHICS_DIR, tmpimg))
        return (plt)
        """