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

## :link: Prerequisite
Operating Systems |
| :---:
  - [x] Microsoft Windows 10 ( _recommended_ )
  - [x] Linux
  - [x] MacOS

Web Browsers |
| :---:
  - [x] Google Chrome ( _highly recommended_ ) 
  - [x] Firefox
  - [x] Microsoft Edge

Intergrated Development Environment (IDE) |
| :---:
   - [x] Any IDE's can be chosen (Visual Studio Code, IntelliJ IDEA, Atom, NetBeans etc)



## :wrench: Installation Setup
Before getting started with the project and interacting through the CLI (Command Prompt / Terminal Window), few procedures must be done on the [**Google Developer**](https://developers.google.com/) platform: 

### Step 1 ) Create a "Programmable Search Engine" 
* Heading here: https://programmablesearchengine.google.com/about/ will take you to the Google's PSE about page. 
* You will need to click on "Get Started" and follow along with the next set of on-screen instructions

### Step 2 ) Acquire the "API Key"
* After creating the personalised PSE, head over to the 'Custom Search JSON API' page to get an API key which you can click from here to make one:  https://developers.google.com/custom-search/v1/overview 

### Step 3 ) Next, configure a "Virtual Environment":
 * VEs manage dependencies for a particular project
   * Packages installed for this project will not affect other Python projects or the wide operating system’s packages
 
 #### Create Virtual Environment through Command-Line:
   * `$ mkdir myproject`
   * `$ cd myproject`
   * `$ python3 -m venv venv`
   * _On Windows:_ `> py -3 -m venv venv`
   
 #### Activate VE on Machine:  
   * `$ . venv/bin/activate`
   * _On Windows:_ `venv\Scripts\activate`

### Step 4 ) Through the CLI, install the below named modules on the VE:

_#_ | Module Packages | Supported Version | Module Pip Commands | PyPI Repo
| :---: | :---: | :---: | :---: | :---: |
 1  | [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask "To Flask website")  | v 1.0 + | `pip install Flask` | https://pypi.org/project/Flask/
 2  | [Google Search API](https://github.com/googleapis/google-api-python-client "Official Google Search API GitHub repo")| v 1.12 |`pip install google-api-python-client`| https://pypi.org/project/google-api-python-client/
 3  | [Requests](https://requests.readthedocs.io/en/master/user/install/ "Requests website") | v 2.25 +  | `pip install requests` | https://pypi.org/project/requests/
 4  | [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html "BeautifulSoup site") | v 4.9 + | `pip install beautifulsoup4` | https://pypi.org/project/beautifulsoup4/
 5  | [Natural Lanaguge Toolkit](https://www.nltk.org/install.html "Official NLTK website") | v. 3.5+  | `pip install nltk` | https://pypi.org/project/nltk/
 6  | [WordCloud](https://amueller.github.io/word_cloud/https://pypi.org/project/wordcloud/ "WordCloud") | v. 1.8 | `pip install wordcloud`| https://pypi.org/project/wordcloud/
 7  | [Matplotlib][(https://matplotlib.org/) | v 3.3 | `pip install matplotlib` | https://pypi.org/project/matplotlib/
 8  | [NumPy](https://numpy.org/) | | `pip install numpy` | https://pypi.org/project/numpy/
 8  | [SciPy](https://www.scipy.org/) | | `pip install scipy` | https://pypi.org/project/scipy/

## :grey_exclamation: Notes
 * Both [`Python`](https://www.python.org/downloads/) and [`pip`](https://packaging.python.org/tutorials/installing-packages/) packages must be pre-installed too - [`Python 3.4+`](https://www.python.org/downloads/release/python-340/) by default comes with the **pip install manager**
 
 * The [`wordcloud`](https://pypi.org/project/wordcloud/) module depends on: [`numpy`](https://numpy.org/install/) and [`pillow`](https://pillow.readthedocs.io/en/stable/installation.html) as well as [`matplotlib`](https://matplotlib.org/users/installing.html) 

_For more information on these modules, please visit their respective websites by clicking on the hyperlinks_


## License
---
