LOCAL ALIGNMENT APPLICATION
===========================

This application is intended to display how similar are 2 Gen Strings
based on the substring with the highest score found by the algorithm
Smith-Waterman.

The application has been developed on Flask Framework so it can be deployed
on Heroku and be used from anywhere.

INSTALLATION REQUIREMENTS
=========================

The application has been developed on Python2.7, so before running the application
make sure you have it installed.

Select the environment for the application:
    * source flask/bin/activate
    * NOTE: environment for flask web framework has been added to the github repository to facilitate the process.
    
Install virtualenv
    * For OSx: sudo easy_install virtualenv
    * For Linux:  sudo apt-get install python-virtualenv
    * virtualenv flask

Install Flask framework:
    * pip install -r requirements.txt
    
To start the application, it's required to execute the following command:
    * ./run.py

If the application is executed in a local environment, the url is:
    * http://0.0.0.0:3609/
