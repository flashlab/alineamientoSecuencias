Install Python 3

If you type


$ brew search python
1
$ brew search python
you will see the available python-related packages to install, and python3 should be among them. Let’s install it!


$ brew install python3
1
$ brew install python3
You can check which version is installed by typing


$ python3 --version
1
$ python3 --version
And you can open it with:


$ python3
1
$ python3
Moreover, when you install python with Homebrew, you also install:

the corresponding pip package manager, which is called pip3
the corresponding Setuptools
pyvenv, and alternative to virtualenv — cool!!
Create Virtual environments with pyvenv

Now that you have Python3 you also have pyvenv, a tool to create virtual environments (similar to virtualenv). However, there is one important remark about the version of pyvenv you have installed: only if you installed Python 3.4 or latter, pyvenv will also install pip when creating a new virtual environment.

Let’s create a new virtual envirnoment, named myenv, using pyvenv:


$ pyvenv myenv
1
$ pyvenv myenv
This will create a folder named myenv in the current directory. To activate this environment just type:

$ source myenv/bin/activate
1
$ source myenv/bin/activate
and you can start Python 3 by just typing:

$ python
1
$ python
Note that as you are inside the virtual environment, you don’t need to use the command python3 to open Python 3.

http://www.marinamele.com/2014/07/install-python3-on-mac-os-x-and-use-virtualenv-and-virtualenvwrapper.html
Create Environment

pyvenv Environment
source envP/bin/activate
pip install cherrypy

Install pip > sudo easy_install pip
# Install cherrypy > pip install cherrypy
Install django > pip install django
pyv

https://docs.djangoproject.com/en/1.10/intro/tutorial01/