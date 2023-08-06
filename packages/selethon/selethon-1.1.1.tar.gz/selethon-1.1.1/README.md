# Selethon

The greatest automated browser controller using Selenium.

### Installing

First, install this project by pip

```
pip install selethon
```

Download webdriver for selethon

```
selethon install chrome
```

## Documentation
Init the browser by
```python
from selethon import Selethon

browser = Selethon()
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

