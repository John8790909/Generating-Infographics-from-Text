# Generating Infographics from Text #
~ ~ ~ BSc (Hons) Computer Science | Yr 3 Lvl 6 - Project ~ ~ ~


An automated-based system that allow user(s) to enter a search query on an interactive form. This webscraps data from multiple URLs using  **Google Search Application Programming Interface** [(GS API)](https://github.com/googleapis/google-api-python-client "Click to see more info about GS API"), preprocesses the retrieved HTML pages into a **cleaned data** presentable format, applies **Natrual Language Processing** [(NLP)](https://en.wikipedia.org/wiki/Natural_language_processing "Click for more info in NLP") operations to the dataset and generates a visualised informational graphic (_a.k.a. "infographic"_) as the resulted output.

## :page_facing_up: Description
GIFT is scripted in the [Python](https://www.python.org/) programming language at the back-end server-side.
With the use of simple micro web framework, [Flask](https://pypi.org/project/Flask/), the system is presented and deployed in a webpage -
structured in [HTML5](https://www.w3.org/standards/webdesign/htmlcss) and styled with [CSS3](https://www.w3.org/standards/webdesign/htmlcss)

The app includes:
  * Google Custom Search API (GCS API) / Custom Search API (CS API)
    * Providing 100 search queries to be used for free on the system per day
  * Programmable Search Engine (formerly known as Google Custom Search Engine / GCS & Google Co-op)
    * Manipulating information in web searches; refining and categorising queries of the user search input 

## :link: This application supports:
  - [x] Python version 3.5, 3.6, 3.7, or 3.8
  - [x] Flask version preferably 1.0+
  - [x] NLTK version 3.5


## :wrench: Installation Setup
Using Python Package Manager (PIP), you will need to install the following on your machine's CLI (_Command Prompt / Terminal Window_): 

_#_ | Module Packages | CLI Commannds | Module Websites
 | :---: | :---: | :---: | :---:
 1  |  Flask                       | `pip install Flask`                        | [Official Flask site](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask)
 2  |  Google Search API           | `pip install google-api-python-client`     | [Official Google API repo](https://github.com/googleapis/google-api-python-client)
 3  |  Requests                    | `pip install requests`               | [Official Requests site](https://requests.readthedocs.io/en/master/user/install/)
 4  |  BeautifulSoup               | 'pip install beautifulsoup4          | [Official BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html)
 3  |  Natural Lanaguge Toolkit    | `pip install nltk`                   | [Official NLTK site](https://www.nltk.org/install.html)
 4  |  WordCloud                   | `pip install wordcloud`              | [Official WordCloud site](https://amueller.github.io/word_cloud/https://pypi.org/project/wordcloud/)



## :grey_exclamation: Notes
 * Both [`Python`](https://www.python.org/downloads/) and [`pip`](https://packaging.python.org/tutorials/installing-packages/) packages must be pre-installed too - [`Python 3.4+`](https://www.python.org/downloads/release/python-340/) by default comes with the **pip install manager**
 
 * The [`wordcloud`](https://pypi.org/project/wordcloud/) module depends on: [`numpy`](https://numpy.org/install/) and [`pillow`](https://pillow.readthedocs.io/en/stable/installation.html) as well as [`matplotlib`](https://matplotlib.org/users/installing.html) 

For more information on these modules, please visit their respective websites by clicking on the hyperlinks


## License
--
