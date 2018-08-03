# tinyurls

URL shortening service to be used in a microservices environment.


## Installation
Use virtual environment
```bash
virtualenv env
source env/bin/activate

```
Change into tinyurls directory and install
```
cd tinyurls
python setup.py install 

```

## Execute
```bash
tinyurls -h
usage: tinyurls [-h] [-p PORT] [-d DATABASE]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port used for this service
  -d DATABASE, --database DATABASE Database to use


tinyurls -p 8888
```





