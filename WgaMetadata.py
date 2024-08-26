import os
import json

class WgaMetadata():
    def __init__(self,metadataPath) -> None:
        self.metadataPath=metadataPath
        if os.path.exists(metadataPath):
            with open(metadataPath,'r',encoding='utf-8') as metadataFile:
                self.metadata:list=json.loads(metadataFile.read())
        else:
                self.metadata={}
                
    def writeMetadata(self,key,dict):
        self.metadata[key]=dict
    
    def dumpMetadata(self):
        with open(self.metadataPath,'w',encoding='utf-8') as metadataFile:
            metadataFile.write(json.dumps(self.metadata))

if __name__=="__main__":
    metadata=WgaMetadata('metadata.json')
    metadata.writeMetadata('q',{'b':'a'})
    metadata.dumpMetadata()
    print(metadata.metadata)