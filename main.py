from WgaParser import WgaParser
from WgaTsv import WgaTsv
from WgaFetcher import WgaFetcher,IMAGE_DIR
import argparse

argparser=argparse.ArgumentParser(
            prog='WgaScraper',
            description='Collects artworks from the Web Gallery of Art',
            )
# Add optional quality param, defaults to high quality
argparser.add_argument('-low_quality',action='store_false',help='Downloads a lower resolution version of the image, defaults to high quality')
# If we are providing a start index we are not gathering from an individual link
arggroup=argparser.add_mutually_exclusive_group()
arggroup.add_argument('-l','--link',type=str,required=False,help='Scrape a singular link from https://www.wga.hu (e.g https://www.wga.hu/html/a/aachen/j_couple.html)')
arggroup.add_argument('-s','--start',type=int,default=0 ,help='Starts the scraping process at a certain index in the catalog')

args=argparser.parse_args()

# Initilization of the parser object
parser=WgaParser('catalog.txt')
parser.ensureColumnsNotEmpty(
        [
            WgaTsv.author,
            WgaTsv.lifeInfo,
            WgaTsv.title,
            WgaTsv.date,   
            WgaTsv.technique,
            WgaTsv.location,
            WgaTsv.url,
            WgaTsv.form,
            WgaTsv.type,
            WgaTsv.school,
            WgaTsv.timeframe,
        ]
    )
parser.filterForms(["painting","portrait"])

# Instantiate fetcher
fetcher=WgaFetcher()

# If a link is passed we are just scraping one
if args.link:
    index=parser.verifyLinkInCatalog(args.link)
    if index:
        description,path=fetcher.processLink(
            parser.catalog[index][WgaTsv.url.value],
            parser.catalog[index][WgaTsv.author.value],
            parser.catalog[index][WgaTsv.title.value],
            args.low_quality,
        )
        fetcher.metadataObject.writeMetadata(path,{
            "url":parser.catalog[index][WgaTsv.url.value],
            "title":parser.catalog[index][WgaTsv.title.value],
            "author":parser.catalog[index][WgaTsv.author.value],
            "date":parser.catalog[index][WgaTsv.date.value],
            "technique":parser.catalog[index][WgaTsv.technique.value],
            "timeframe":parser.catalog[index][WgaTsv.timeframe.value],
            "school":parser.catalog[index][WgaTsv.school.value],
            "type":parser.catalog[index][WgaTsv.type.value],
            "description":description,
        })
        fetcher.metadataObject.dumpMetadata()
        print(path,description)
    else:
        raise ValueError("Link not present in catalog.txt")
    
# If no link is passwed we are scraping the entire catalog
else:
    if args.start>len(parser.catalog):
        raise IndexError(f"The index you provided is out of range, It must be greater than 0 and less than {len(parser.catalog)}")
    # Get the data
    for entry in parser.catalog[args.start:]:
        description,path=fetcher.processLink(
            entry[WgaTsv.url.value],
            entry[WgaTsv.author.value],
            entry[WgaTsv.title.value],
            args.low_quality,
        )
        fetcher.metadataObject.writeMetadata(path,{
            "url":entry[WgaTsv.url.value],
            "title":entry[WgaTsv.title.value],
            "author":entry[WgaTsv.author.value],
            "date":entry[WgaTsv.date.value],
            "technique":entry[WgaTsv.technique.value],
            "timeframe":entry[WgaTsv.timeframe.value],
            "school":entry[WgaTsv.school.value],
            "type":entry[WgaTsv.type.value],
            "description":description,
        })
        fetcher.metadataObject.dumpMetadata()
        