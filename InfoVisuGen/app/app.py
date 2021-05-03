# -*- coding: utf-8 -*-
# app.py : Application's Main Script


''' Imports modules/libraries '''
import os, re
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from query_extractor import QueryExtractor
import query_extractar
from wordcloud_generator import WordcloudGenerator
from worldmap_visualiser import MapVisualiser

# from flask_cors import CORS
# from forms import SignUpForm
# from flask_sqlclchemy import SQLAlchemy
# from wtforms import Form, StringField
# from flask import redirect, request, session


#-- Flask stores session in a cookie. In order to keep the session safe, it "signs" it
#-- So that the signature can be verified after each request to check that the data hasn't be tampered woth
#-- Secret key is used ro sign cookie

''' Sets path names of different folders/directories '''
APP_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
TEMPLATE_DIR = os.path.abspath('../templates/')              
IMG_DIR = os.path.join(STATIC_DIR, 'img')                  # sets nested "img" folder path
INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics')    # creates folder named "infographics"


''' Creates a Flask app instance and secret key '''
app = Flask(__name__) 
app.config['SECRET_KEY'] = 'adgjl2468'

# CORS(app)
# app.config.form_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.permanent_session_lifetime = timedelta(minutes=5)
# db = SQLAlchemy(app)


''' Flask endpoints defined with View functions being intialised '''
# Webapp server/
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Webapp server/about     
@app.route("/about")
def about():
    # return "This is the about page"
    return render_template("about.html")

# Webapp server/text-mining-info 
@app.route("/nlp")
def nlp():
    return render_template('nlp.html')

# Webapp server/generator   
@app.route("/generator", methods = ['GET', 'POST'])
def generator():
    
    # if the request method is achieved through POST, grabs specfiied submission of HTML form-data: "searchInput" 
    # & validates the the text input, once it's accepted, "query_results()" is then called..

    if request.method == "POST":
        userinput = request.form["searchInput"]
        flash("You have entered, ", userinput)  # return "OK", 200
        
        if not userinput:
            flash("Ooof! You must submit something, Sorry!, 'error'")
            return render_template("generator.html")

        elif not(4 <= len(userinput) <= 40):
            flash("Your input search query must be between 4 and 40 characters long in length !!, 'error'")
            return render_template("generator.html")
        
        # checks entry if it doesn't contain any lower/uppercase characters (including white spaces)
        elif not(re.match(r'^([a-zA-Z ])+$', userinput)):
            flash(" @!?£*-+=/$%^&()<>`¬ Not Accepted !! Your input search query must only contain alphabetic characters !!!")
            return render_template("generator.html")
        
        else:
            # the user input is validated, calls query_results() 
            flash("Submission Success! Hold-on, We're Processing your search query...")
            return run_wordcloud_operations(userinput)
            
            """ if "wordcloud" in request.form:
                return run_wordcloud_operations(userinput)
            elif "worldmap" in request.form:
                return run_worldmap_operations(userinput) """

    # form wasn't submitted, simply renders page
    else:
        return render_template("generator.html")


''' Finds relevant google search result links based on the query - an object, qe, is instantiated from QueryExtractor 
and series of class instance methods are called; List of relevant search results URL are then retrieved ; 
content of extracted website data are manipulated & Preprocessed with Natrual Language Processing module 
and a Wordcloud visual, of varying word size, is then propoerly generated '''

def run_wordcloud_operations(query):

    query_results = query_extractar.get_query_results(query, num_results=1, pause=2)
    extracted_data = query_extractar.extract_web_data(query_results)
    preprocessed_data = query_extractar.preprocess_raw_text(extracted_data)
    named_entities = query_extractar.locate_named_entities(preprocessed_data)
    named_entities_freq = query_extractar.contruct_ne_freq_dict(named_entities)
    top_freq_elements = query_extractar.get_top_freq_entities(named_entities_freq)

    tmpimg_wc = 'wordcloud.jpg'             # passes in a temporary blank image file
    wcg = WordcloudGenerator()
    wcg.generate_simple_wordcloud(tmpimg_wc, named_entities_freq)

    return redirect(url_for('generator'))


''' Find relevant google search result links based on the query an object, qe, is instantiated 
From class QueryExtractor and series of class instance methods are called to be executed
List of relevant search results URL are retrieved, content of extracted website data are manipulated & Preprocessed 
with Natrual Language Processing module --- Worldmap visual is then displayed with retrived country places mapped '''

def run_worldmap_operations(query):
    mv = MapVisualiser()

    query_results = query_extractar.getQueryResults(query, num_results=1, pause=2)
    extracted_data = query_extractar.extractWebData(query_results)
    preprocessed_data = query_extractar.preprocessRawText(extracted_data)
    located_named_entity = query_extractar.locate_named_entities(preprocessed_data)

    mv.show_countries()
    recoupedCountries = mv.check_countries(located_named_entity)
    countriesDataframe = mv.create_countries_dataframe(recoupedCountries)
    countriesContinent = mv.get_continent(countriesDataframe)
    countriesLongLat = mv.geolocate(countriesContinent)
    mv.generate_worldmap(countriesLongLat)

    return redirect(url_for('generator'))


''' class SearchQueryForm(Form):
  submission = StringField("Submission", validators=[InputRequired(), 
  Length(min=4, max=40), Regexp((re.match(r'^([a-zA-Z ]+$')])

def process_input():
    form = SearchQueryForm(request.form)
    if request.method == 'POST' and form.validate():
        user_input = form.submission.data
        flash("Submission Success! Hold-on, We're Processing your search query...")
        return query_results(userInput)
'''

# Webapp server/futurework 
@app.route("/futurework")
def futurework():
    return render_template('futurework.html')

# Webapp server/<query>
# @app.route("/infogen/<query>")
# Webapp server/resultsgen
@app.route("/resultsgen")
def resultsgen():
    return render_template("resultsgen.html")

# Webapp server/searchresults
@app.route("/searchresults")
def searchresults():
    return render_template("searchresults.html")

@app.route('/generator/<string:query>')
def input_api(query):
    if len(query) == 0:
        return flask.jsonify({'status': 'error'})

    return flask.jsonify({'status': 'success'})


if __name__ == "__main__" :
    # Launches Flask dev server
	app.run(debug=True)