from WgaParser import WgaParser
from WgaTsv import WgaTsv
from WgaFetcher import WgaFetcher,IMAGE_DIR
import argparse

argparser=argparse.ArgumentParser(
            prog='WgaScraper',
            description='Collects artworks from the Web Gallery of Art',
            )

argparser.add_argument('-l','--link',required=False)
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
            parser.catalog[index][WgaTsv.title.value]
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
    # Get the data
    for entry in parser.catalog:
        description,path=fetcher.processLink(
            entry[WgaTsv.url.value],
            entry[WgaTsv.author.value],
            entry[WgaTsv.title.value]
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
        