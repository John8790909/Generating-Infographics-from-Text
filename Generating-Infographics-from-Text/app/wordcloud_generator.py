#------------------------------------------------------------------------------------------------
#-- Healal Mushed Uddin | 18007361 | 6G6Z1101 Project MS.04 | Generating Infographics from Text
#------------------------------------------------------------------------------------------------

import os, numpy as np, matplotlib
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from scipy.ndimage import gaussian_gradient_magnitude
from matplotlib import pyplot as plt
from PIL import Image

''' Global Variables '''
APP_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'img')                  # sets nested "img" folder path
INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics')   # creates folder named "infographics"

''' "WordcloudGenerator" class '''
class WordcloudGenerator():
    def __init__(self):
        self.stopwords = set(STOPWORDS)
    
    ''' Generates a visual figure, rendering that image as a wordcloud graphic which contains frequent tokens '''   
    def generate_simple_wordcloud(self, imgWordCloud, ne_freq_dict):
        
        # generates an instantiated wordcloud object with defined properties set
        wordcloud = WordCloud(width=1000, height=1000, max_words=1000, margin=10, background_color="white", random_state = 1)
        print("\n\n", ne_freq_dict, "\n\n")
        wordcloud.generate_from_frequencies(ne_freq_dict)

        # saves the generated plot figure as an image file in current directory
        wordcloud.to_file(os.path.join(INFOGRAPHICS_DIR, imgWordCloud))
        return wordcloud

    ''' Generates a visual figure, rendering that image as a wordcloud graphic which contains frequent tokens '''   
    def create_masked_wordcloud(self, imgWordCloud, ne_freq_dict):
        bubbleimg = np.array(Image.open(os.path.join(INFOGRAPHICS_DIR, 'bubblemask.jpg')))

        # colour white is masked out from the bubble
        bubblemask = bubbleimg.copy()
        bubblemask[bubblemask.sum(axis=2) == 0] = 255

        # filtered array with the use of multidimentional gradient magnitude using Gaussian derivatives
        edges = np.mean([gaussian_gradient_magnitude(
                        bubblemask[:,:,i] / 255., 2) for i in range(3)], axis=0)
        bubblemask[edges > .08] = 255

        # generates an instantiated wordcloud object with defined properties set
        wc = WordCloud(width=1000, height=1000, max_words=1000, margin=10, background_color="grey", 
                        random_state=1, stopwords=self.stopwords, mask=bubblemask)

        wc.generate_from_frequencies(ne_freq_dict)
        wc.to_file(os.path.join(INFOGRAPHICS_DIR, 'bubblemaskedwordcloud.jpg'))

        # creates colourised wordcloud from generated plot figure
        image_colours = ImageColorGenerator(bubbleimg)
        wc.recolor(color_func=image_colours)
        wc.to_file(os.path.join(INFOGRAPHICS_DIR, "bubblemaskedcolouredwordcloud.jpg"))

        return wc

    def create_flag_masked_wordcloud(self, imgWordCloud, ne_freq_dict):
        flagimg = np.array(Image.open(os.path.join(INFOGRAPHICS_DIR, 'ukflag.jpg')))
        wc = WordCloud(width=500, height=500, max_words=1000, margin=10, random_state=42, background_color="grey",
                        stopwords=self.stopwords, mask=flagimg)
        
        wc.generate_from_frequencies(ne_freq_dict)
        wc.to_file(os.path.join(INFOGRAPHICS_DIR, 'ukflagmaskedcolouredwordcloud.jpg'))
        return wc

    def create_map_masked_wordcloud(self, imgWordCloud, ne_freq_dict):
        mapimg = np.array(Image.open(os.path.join(INFOGRAPHICS_DIR, 'ukmap.jpg')))
        wc = WordCloud(width=500, height=500, max_words=1000, margin=10, random_state=42, background_color="grey",
                        stopwords=self.stopwords, mask=mapimg)
        
        wc.generate_from_frequencies(ne_freq_dict)
        wc.to_file(os.path.join(INFOGRAPHICS_DIR, 'ukmapmaskedcolouredwordcloud.jpg'))
        return wc
        