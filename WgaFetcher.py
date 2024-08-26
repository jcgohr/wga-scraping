import requests
import urllib.request
import os
from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from WgaMetadata import WgaMetadata

IMAGE_DIR='images/'
METADATA_PATH='metadata.json'

class WgaFetcher():
    def __init__(self) -> None:
        # Make image directory
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)
        self.metadataObject=WgaMetadata(METADATA_PATH)
    
    def requestPage(self,link)->BeautifulSoup:
        response=requests.get(link)
        if response.status_code==429:
            timeouts=1
            while response.status_code==429:
                timeout=timeouts*30
                print(f"Request timed out, waiting {timeout} seconds")
                sleep(timeout)
                timeouts+=1
                response=requests.get(link)
                
        if response.content==None:
            raise ValueError("No content contained in response")
        
        return BeautifulSoup(response.content)
    
    def fetchImage(self,link,downloadPath):
        # Bypasses the start of the link (https://www.wga.hu/html) and erases the ".html" extension
        pagePath=link[24:-5]
        # We assume every image is a .jpg file but error handling is included
        response=urllib.request.urlretrieve(f"https://www.wga.hu/detail/{pagePath}.jpg",downloadPath)
        # Check if image exists, raise exception if it doesn't
        if not os.path.exists(downloadPath):
            raise urllib.request.HTTPError(msg=f"No image downloaded for {link}")
      
        
    def extractDescription(self,soup:BeautifulSoup,link:str)-> str | None:
        # Filter <td>'s for a string that signifies the start of a description
        tds=[td for td in soup.find_all('td') if " Comment Start " in td.contents]
        lengthTds=len(tds)
        if lengthTds==0:
            print(f"No description found for {link}")
            return None
        elif lengthTds>1:
            raise Exception(f"More than one comment found, You should visit {link} and inspect the page")
        return tds[0].text
    
    def processLink(self,link,artistName:str,artworkName:str)->tuple[str,str]:
        """
        runs fetchImage and extractDescription with a single call
        """
        sanitizedArtworkName=sanitize_filename(artworkName)
        artistPath=f'{IMAGE_DIR}{sanitize_filename(artistName)}/'
        # Make artist directory
        if not os.path.exists(artistPath):
            os.mkdir(artistPath)
        artPath=artistPath+sanitizedArtworkName+'.jpg'
        if not os.path.exists(artPath):
            self.fetchImage(link,artPath)
        else:
            # This solution is only effective for pieces with the same title, It will re-download exisiting pieces
            # Another method of detecting previously downloaded images is required
            duplicateNameCounter=1
            artPath=artistPath+sanitizedArtworkName+f' ({duplicateNameCounter})'+'.jpg'
            while os.path.exists(artPath):
                duplicateNameCounter+=1
                artPath=artistPath+sanitizedArtworkName+f' ({duplicateNameCounter})'+'.jpg'
            self.fetchImage(link,artPath)
            
        page=self.requestPage(link)
        description=self.extractDescription(page,link)
        return description,artPath
    
if __name__=="__main__":
    fetcher=WgaFetcher()
    print(fetcher.processLink("https://www.wga.hu/html/r/raphael/2firenze/1/23connes.html"))
