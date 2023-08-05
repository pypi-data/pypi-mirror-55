# Selenus

The greatest automated browser controller using Selenium.


## Prerequisites

This program needs Python 3 and following libraries

* [WebDriverManager](https://pypi.org/project/webdrivermanager/) - Webdriver manager for Python


### Installing

First, install this project by pip

```
pip install selenus
```

Download webdriver for selenus

```
selenus webdriver chrome
```

## Documentation
Init the browser by
```python
from selenus import Selenus

browser = Selenus()
```

Open the url
```python
browser.open("https://www.google.com")
```

Type text into input
```python
browser.type("input.gLFyf", "thanawatpetchuen site:github.com")
```

Click element
```python
browser.click("div.FPdoLc>center>input:nth-child(1)")
```

## Authors

* **Thanawat Petchuen** - [Thanawat(GitHub)](https://github.com/thanawatpetchuen) - [Thanawat(Bitbucket)](https://bitbucket.org/thanawatpetchuen/) 


## License

This project is licensed under the MIT License 

