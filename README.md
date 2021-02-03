# Generating Infographics from Text #
~ ~ ~ BSc (Hons) Computer Science | Yr 3 Lvl 6 - Project ~ ~ ~


An automated-based system that allow user(s) to enter a search query on an interactive form. This webscraps data from multiple URLs using  **Google Search Application Programming Interface** [(GS API)](https://github.com/googleapis/google-api-python-client "Click to see more info about GS API"), preprocesses the retrieved HTML pages into a **cleaned data** presentable format, applies **Natrual Language Processing** [(NLP)](https://en.wikipedia.org/wiki/Natural_language_processing "Click for more info in NLP") operations to the dataset and generates a visualised informational graphic (_a.k.a. "infographic"_) as the resulted output.

## :page_facing_up: Description
GIFT is scripted in the [Python](https://www.python.org/) programming language at the back-end server-side.
With the use of simple micro web framework, [Flask](https://pypi.org/project/Flask/), the system is presented and deployed in a webpage -
structured in [HTML5](https://www.w3.org/standards/webdesign/htmlcss) and styled with [CSS3](https://www.w3.org/standards/webdesign/htmlcss)

The app includes:
  * **Google Custom Search API** (GCS API) / Custom Search API (CS API)
    * Providing 100 search queries to be used for free on the system per day
  * **Programmable Search Engine** (formerly known as Google Custom Search Engine / GCS & Google Co-op)
    * Manipulating information in web searches; refining and categorising queries of the user search input 

## :link: Supports:
Operating Systems |
| :---:
  - [x] Microsoft Windows 10 (_recommended_)
  - [x] Linux
  - [x] MacOS

Web Browsers |
| :---:
  - [x] Google Chrome (_highly recommended_)
  - [x] Firefox
  - [x] Microsoft Edge


## :wrench: Installation Setup
Step 1 ) You will need to configure a **Virtual Environment** in your machine through the CLI (_Command Prompt / Terminal Window_): 
 * VEs manage dependencies for a particular project
  * Packages installed for this project will not affect other Python-based projects or the wide operating system’s packages
 
 1.1) * Creating a Python Virtual Environment:
   * `$ mkdir myproject`
   * `$ cd myproject`
   * `$ python3 -m venv venv`
   * On Windows:`$ py -3 -m venv venv`

Step 2 ) Using Python Package Manager (PIP), install the below named modules:

_#_ | Module Packages | Supported Version | CLI Commannds | PyPI Repo
| :---: | :---: | :---: | :---: | :---: |
 1  | [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask)  | v 1.0 + | `pip install Flask` | https://pypi.org/project/Flask/
 2  | [Google Search API](https://github.com/googleapis/google-api-python-client)| v 1.12 |`pip install google-api-python-client`| https://pypi.org/project/google-api-python-client/
 3  | [Requests](https://requests.readthedocs.io/en/master/user/install/) | v 2.25 +  | `pip install requests` | https://pypi.org/project/requests/
 4  | [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html) | v 4.9 + | `pip install beautifulsoup4` | https://pypi.org/project/beautifulsoup4/
 5  | [Natural Lanaguge Toolkit](https://www.nltk.org/install.html) | v. 3.5+  | `pip install nltk` | https://pypi.org/project/nltk/
 6  | [WordCloud](https://amueller.github.io/word_cloud/https://pypi.org/project/wordcloud/) | v. 1.8 | `pip install wordcloud`| https://pypi.org/project/wordcloud/



## :grey_exclamation: Notes
 * Both [`Python`](https://www.python.org/downloads/) and [`pip`](https://packaging.python.org/tutorials/installing-packages/) packages must be pre-installed too - [`Python 3.4+`](https://www.python.org/downloads/release/python-340/) by default comes with the **pip install manager**
 
 * The [`wordcloud`](https://pypi.org/project/wordcloud/) module depends on: [`numpy`](https://numpy.org/install/) and [`pillow`](https://pillow.readthedocs.io/en/stable/installation.html) as well as [`matplotlib`](https://matplotlib.org/users/installing.html) 

For more information on these modules, please visit their respective websites by clicking on the hyperlinks


## License
--
