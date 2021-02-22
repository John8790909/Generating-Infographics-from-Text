#------------------------------------------------------------------------------------------------
#-- Healal Mushed Uddin | 18007361 | 6G6Z1101 Project MS.04 | Generating Infographics from Text
#------------------------------------------------------------------------------------------------

#!/usr/bin/Python
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, redirect, url_for, request, url_for
from query_extractor import QueryExtractor
from wordcloud_generator import WordcloudGenerator

# from forms import SignUpForm
# from flask_sqlclchemy import SQLAlchemy
# redirect, request, session
#app.secret_key = "-"
#app.permanent_session_lifetime = timedelta(minutes=5)

#-- Sets path names of different folders/directories
APP_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(APP_DIR, 'static')
IMG_DIR = os.path.join(STATIC_DIR, 'img')                  # sets nested "img" folder path
INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics')    # creates folder named "infographics"


# STATIC_DIR = os.path.abspath('../static')
# TEMPLATE_DIR = os.path.abspath('../templates/')              
# IMG_DIR = os.path.join(STATIC_DIR, 'img', "")                  # sets nested "img" folder path
# INFOGRAPHICS_DIR = os.path.abspath('../static/img/infographics/')    # creates folder named "infographics"
# INFOGRAPHICS_DIR = os.path.join(IMG_DIR, 'infographics', "")

#-- Creates a Flask app instance
app = Flask(__name__) 

# app.config.form_object(os.environ['APP_SETTINGS'])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# webapp server/
@app.route("/")
def home():
    return render_template("home.html")

# webapp server/about     
@app.route("/about")
def about():
    # return "This is the about page"
    return render_template("about.html")

# webapp server/infogen   
@app.route("/infogen", methods = ['GET', 'POST'])
def infogen():
    # if the request method is achieved through POST
    if request.method == "POST":
        # grabs specfiied "userquery" from a HTML form attribute
        userinput = request.form["searchInput"]
        processed_text = str(userinput)
        #print(userinput.get_text())
        # return "OK", 200

        # once the input's been retrieved, and submit button's been clicked
        #  redirects user to another page defined in "query_results" method with passed "query"
        return redirect(url_for("query_results", query=userinput))
    
    # else simply render page
    else:
        return render_template("infogen.html")
    



# webapp server/<query>
@app.route("/infogen/<query>")
def query_results(query):

    # find relevant google search result links based on the query
    # an object, qe, is instantiated from class QueryExtractor and class methods are executed
    # list of query results are retrieved, preprocessed with NLP operations along with content of extracted webpage data being outputted 
    
    qe = QueryExtractor()
    wcg = WordcloudGenerator()
    query_results = qe.get_query_results(query)
    extracted_data = qe.extract_webdata()
    preprocessed_data = qe.preprocess_textdata()
    counted_entities_frequency = qe.count_entities_frequency()

    tmpimg = 'wordcloud.jpg'                        # passes in the filename to generate a wordcloud using the temporary image file
    wcg.generate_simple_wordcloud(tmpimg, counted_entities_frequency)
    
    # generated_wordcloud = qe.generate_wordcloud(tmpimg)
    # masked_wordcloud = qe.create_masked_wordcloud(tmpimg)
    # generated_wordcloud = wcg.generate_wordcloud(tmpimg)
    # masked_wordcloud = wcg.create_masked_wordcloud(tmpimg)

    return render_template("/infogen.html", q = f"{query}", qr = query_results, 
                                ed = extracted_data, ppd = preprocessed_data, 
                                    cef = counted_entities_frequency)


# webapp server/searchresults
@app.route("/resultsgen")
def resultsgen():
    return render_template("resultsgen.html")


# webapp server/searchresults
@app.route("/searchresults")
def searchresults():
    return render_template("searchresults.html")


# webapp server/text-mining-info 
@app.route("/textmininginfo")
def textmininginfo():
    return render_template('textmininginfo.html')

# webapp server/futurework 
@app.route("/futurework")
def futurework():
    return render_template('futurework.html')

# webapp server/search.html 
@app.route("/search")
def search():
    return render_template('search.html')

# webapp server/search-result.html 
@app.route("/search-result")
def searchresult():
    return render_template('search-result.html')


if __name__ == "__main__" :
    
    # Launches Flask dev server
	app.run(debug=True)


# f = open("/searchresults.html", "wb")
#     message = """ 
#         <html> 
#             <head> </head>
#             <body> {j} </body>
    
#     """
#     f.write(message)
#     f.close() 

# def execute_query_results(query):
    #     query_results = []
    #     for j in gsearch(query, tld="com", lang="en", num=10, stop=10, pause=2):
    #         query_results.append(j)
    #         print(j)
    #     return query_results 


# return f"""
        # <h1 style="text-align:center"> Search Query Results </h1>
        # <br> <h3 style="text-align:center"> This is your query: <strong><i>'{query}'</i></strong> </h3> 
        # <br> <p><strong> Here are all the relevant search results URL based on your query: </strong> <br> '{query_results}' </p> """
        # <br> <p><strong> And here is the extracted data from each link: </strong><br> '{extracted_data}' </p>
        # <br> <p><strong> The following are the preprocessed text data using Natural Language Processing: </strong><br> '{preprocess_data}'</p>
        # <br> <p><strong> Visualised Wordcloud of the most frequent entities processed from the results of the search query: </strong><br> '{generated_wordcloud}' </p>
      
# <!-- <table style="border:'1'">
        #     <caption> Search Results </caption>
        #     {% for key, value in result.items() %}
        #     <tr>
        #         <th> {{ key }} </th>
        #         <td> {{ value }} </td>

        #     </tr>
        #     {% endfor %}
# </table> -->