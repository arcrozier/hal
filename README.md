# HAL
A chatbot to emulate HAL from *2001: A Space Odyssey*

## Installing Dependencies
This project requires 
[Python](https://www.python.org/downloads/).

From your command line, `cd` into the repo. Once there, run 
`pip install -r requirements.txt`. If that doesn't work, you can also try
`pip3 install -r requirements.txt`, 
`python -m pip install -r requirements.txt`, or
`python3 -m pip install -r requirements.txt`. If that doesn't work,
ensure Python is installed and on your PATH.

## Quickstart Guide
Once you've cloned the repo, all you need to do is `cd` into the repo
from your command line and run `python manage.py runserver`. If it doesn't
work, please ensure Python is on your PATH or try
`python3 manage.py runserver`.

You can then interact with HAL at http://localhost:8000. If port 8000 is in use,
call `runserver` with a port argument: `python3 manage.py runserver <port>`.
Running without specifying a port is the same as `python3 manage.py runserver 8000`.
If you use a different port, make sure you access the site with that port:
http://localhost:&lt;port&gt;
