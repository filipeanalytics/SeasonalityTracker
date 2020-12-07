# SeasonalityTracker
http://filipeanalytics.herokuapp.com/

Python application built in a HTML/CSS page, deployed on Heroku web server. 
It collects data of a specific stock for a specific period from Yahoo Finance and plots multiple candlestick graphs (one plot for each year in the period). 

The only essential files are the python files script.py and StockFunctions3.py, and the static(css file) and templates folder (html files). 
script.py: the API built to communicate with html using "flask" library
StockFunctions3.py: contains all the python code
static folder: contains the CSS file
templates folder: contains the HTML file

Procfile, runtime.txt and requirements.txt are the 3 files required to deploy a python application into Heroku server.
.idea folder: Project settings are stored with each specific project as a set of xml files under the . idea folder.
