from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from WgaMetadata import WgaMetadata
import requests
import urllib.request
import os
import re

IMAGE_DIR='images/'
METADATA_PATH='metadata.json'

def rename_uncased_duplicates(directory,rename=True)-> dict:
    """
    Returns a dictionary of renamed images, the key is the renamed image and the value is the original name
    If rename is set to true the file will be renamed, if set to false nothing will change
    """
    renames={}
    images=os.listdir(directory)
    lower_case_images=[image.lower() for image in images]
    # A dictionary used to keep track of multiple uncased duplicates
    duplicates_dict={}
    for i in range(len(lower_case_images)):
        image=lower_case_images.pop(0)
        # pop the same image from images so that they are aligned
        images.pop(0)
        # This if statement checks that after popping the head of the list its still in the list
        if image in lower_case_images:
            dupe_idx=0
            for idx in range(len(lower_case_images)):
                if lower_case_images[idx]==image:
                    dupe_idx=idx
            image_path=os.path.join(directory,images[dupe_idx])
            renamed_image_path=os.path.join(directory,images[dupe_idx][:-4]+f"(d{duplicates_dict[image] if image in duplicates_dict else ''}).jpg")
            print(f"uncased duplicate found for {image_path}")
            #Rename the file with a (d) for duplicate which makes them different
            if rename:
                os.rename(
                    image_path,
                    # Remove .jpg extension and add uncased duplicate identifier
                    renamed_image_path,                
                )
            # Update duplicate dict
            if image not in duplicates_dict:
                duplicates_dict[image]=1
            else:
                duplicates_dict[image]+=1
            
            renames[renamed_image_path]=image_path
                
    return renames


class WgaFetcher():
    def __init__(self,directory) -> None:
        # Make image directory
        self.directory=directory
        self.im_dir=os.path.join(directory,IMAGE_DIR)
        if not os.path.exists(self.im_dir):
            os.mkdir(self.im_dir)
        self.metadataObject=WgaMetadata(os.path.join(self.directory,METADATA_PATH))
    
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
        
        return BeautifulSoup(response.content,features="html.parser")
    
    def fetchImage(self,link,downloadPath,imageQuality:bool):
        # Bypasses the start of the link (https://www.wga.hu/html) and erases the ".html" extension
        pagePath=link[24:-5]
        # "art" means a higher resolution image and "detail" is a lower res image
        quality="art" if imageQuality else "detail"
        # Retrieve image and assume every image is a .jpg file
        response=urllib.request.urlretrieve(f"https://www.wga.hu/{quality}/{pagePath}.jpg",downloadPath)
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
        
        td = tds[0]
        tables = td.find_all('table')
        for table in tables:
            table.decompose()

        if lengthTds==1:
            return re.sub(r'[\r\n]|\\u[0-9A-Fa-f]{4}|\\\"', ' ', td.text).strip()
        elif lengthTds>1:
            raise Exception(f"More than one comment found, You should visit {link} and inspect the page")
    
    def processLink(self,link,artistName:str,artworkName:str,imageQuality:bool)->tuple[str,str]:
        """
        runs fetchImage and extractDescription with a single call
        """
        sanitizedArtworkName=sanitize_filename(artworkName)
        artistPath=f'{self.im_dir}{sanitize_filename(artistName)}/'
        # Make artist directory
        if not os.path.exists(artistPath):
            os.mkdir(artistPath)
        artPath=artistPath+sanitizedArtworkName+'.jpg'
        if not os.path.exists(artPath):
            self.fetchImage(link,artPath,imageQuality)
        else:
            # This solution is only effective for pieces with the same title, It will re-download exisiting pieces
            # Another method of detecting previously downloaded images is required
            duplicateNameCounter=1
            artPath=artistPath+sanitizedArtworkName+f' ({duplicateNameCounter})'+'.jpg'
            while os.path.exists(artPath):
                duplicateNameCounter+=1
                artPath=artistPath+sanitizedArtworkName+f' ({duplicateNameCounter})'+'.jpg'
            self.fetchImage(link,artPath,imageQuality)
            
        page=self.requestPage(link)
        description=self.extractDescription(page,link)
        return description,artPath
    
if __name__=="__main__":
    fetcher=WgaFetcher()
    print(fetcher.processLink("https://www.wga.hu/html/r/raphael/2firenze/1/23connes.html"))