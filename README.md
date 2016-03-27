# Link Shortener
This is a fun personal project I did to make a link shortener for my personal website. It primarily uses [Bottle](http://bottlepy.org/docs/dev/index.html), [MySQL Connector](http://dev.mysql.com/doc/connector-python/en/), and [bcrypt](https://pypi.python.org/pypi/bcrypt/1.0.2).
## Requirements
You will need to have Python 3, MySQL server, and the necessary Python libraries installed to be able to use this software. I use [UWSGI](https://uwsgi-docs.readthedocs.org/en/latest/) and [NGINX](https://www.nginx.com/resources/wiki/) to host the application. 

To get Python to connect to the MySQL databse you will have to modify the ``mysql.cnf`` [option file](http://dev.mysql.com/doc/refman/5.7/en/option-files.html) to have the settings your MySQL server is using.

The ``secret`` file (used for secure cookies) can be generated automatially when the application first runs if you give write access to the user running your server to the directory that ``app.py`` resides in. However, the secret file can be generated manually by running the following script.

    import os
    f = open("secret","wb")
    f.write(os.urandom(16))
    f.close()

``deploy.sh`` is a utility to copy the files (specified in variables) to their appropriate location (variables again) and restart uwsgi.

``testServer.sh`` is a script to run an instance of UWSGI to test changes to link shortener without affecting the live version of the link shortener. Running ``touch /tmp/app`` will cause this server to reload. Do this to test changes made to the shortener. By default the test server will run on port 8080, but can easly be changed.

## TODO
1. Create a script that wil generate the tables in the database automatically
