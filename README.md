# wga-scraping
A repository for scraping the  [Web Gallery of Art](https://www.wga.hu/).
## Installation
Firstly install all dependencies
```
pip install -r requirements.txt
```
## Usage
### Default
You will have to run `main.py` to collect the artworks. If you run without arguments it will attempt to collect the entire catalog of art as defined in `catalog.txt`.
```
python main.py
```
### Arguments
With arguments you can alter the quality of the downloaded artworks, start at a specific line in `catalog.txt`, or only download a single artwork.
```
python .\main.py --help
usage: WgaScraper [-h] [-low_quality] [-l LINK | -s START]

Collects artworks from the Web Gallery of Art

options:
  -h, --help            show this help message and exit
  -low_quality          Downloads a lower resolution version of the image, defaults to high quality
  -l LINK, --link LINK  Scrape a singular link from https://www.wga.hu (e.g https://www.wga.hu/html/a/aachen/j_couple.html)
  -s START, --start START
                        Starts the scraping process at a certain index in the catalog
```
