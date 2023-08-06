[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

# HTTPserver-mock

a simple http-server mockup to test web crawler.

## Installation
Run the folowing to install:

```shell
pip install HTTPserver-mock
```

## Usage

```python
from src.HTTPserver_mock import HTTPserver_mock
import noizze_crawler as nc


@HTTPserver_mock()
def test_crawler():
    (title, desc, image_url, html) = nc.crawler('http://localhost:8000/index.html')
    print('title:', title)
    print('desc:', desc)
    print('image_url:', image_url)
    print('html:', html[:1000])


if __name__ == '__main__':
    test_crawler()
```

```bash
$ python test.py
127.0.0.1 - - [07/Nov/2019 13:34:55] "GET /index.html HTTP/1.1" 200 -
1573101292.684394 httpserver_mock started
<h2>nope</h2>
1573101296.704611 httpserver_mock finished

```

## ChangeLog
* v2: PyPI published
* v1: Test alpha 

