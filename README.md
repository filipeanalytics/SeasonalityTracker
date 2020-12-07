# SeasonalityTracker
http://filipeanalytics.herokuapp.com/
Python application built in a HTML/CSS page, deployed on Heroku web server. 
It collects data of a specific stock for a specific period from Yahoo Finance and plots multiple candlestick graphs (one plot for each year in the period). 

script.py is the API built to communicate with html using "flask" library, which needs to be installed:
pip install flask

Procfile, runtime.txt and requirements.txt are the 3 files required to deploy a python application into Heroku server.
