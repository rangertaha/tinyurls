# tinyurls

URL shortening service to be used in a microservices environment.

This service does the following:
1. Takes a long url and stores an md5 key and the url in a database table. 
The md5 key is used to lookup the long url. This step returns a short link 
with md5.
2. Takes a short link and redirects you to the long link.





## Installation
Clone code
```bash
git clone git@github.com:rangertaha/tinyurls.git
```
Use virtual environment
```bash
virtualenv env
source env/bin/activate

```
Change into tinyurls directory and install
```
cd tinyurls
python setup.py install 

or

pip install tinyurls

```

## Execute
```bash
tinyurls -h
usage: tinyurls [-h] [-p PORT] [-d DATABASE]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port used for this service
  -d DATABASE, --database DATABASE Database to use


tinyurls -p 9999

```

In a new terminal post the link to shorten
```bash
curl -X POST -H "Content-Type: text/plain" --data "https://www.google.com/search?q=tornado+logging+to+ELK&rlz=1C5CHFA_enUS752US752&oq=tornado+logging+to+ELK&aqs=chrome..69i57.9210j1j4&sourceid=chrome&ie=UTF-8" http://127.0.0.1:9999
http://127.0.0.1:9999/284380fea5eaf2464e06a3873647d324
```

In the browser go to `http://127.0.0.1:9999/284380fea5eaf2464e06a3873647d324`

