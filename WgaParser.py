
from WgaTsv import WgaTsv

class WgaParser():
    """
    Functions dont return the catalog, rather they modify its internal state
    """
    def __init__(self,catalogPath) -> None:
        self.catalog=self.readCatalog(catalogPath)
        
    def readCatalog(self,catalogPath:str):
        with open(catalogPath,'r',encoding='utf-8') as catalogFile:
            return [catalogLine.split('\t') for catalogLine in catalogFile.readlines()]

  
    def ensureColumnsNotEmpty(self,nonEmptyColumns:list):
        """
        Takes the catalog and ensures certain fields aren't empty
        """
        fullRows=[]
        
        for entry in self.catalog:
            addFlag=True
            for field in nonEmptyColumns:
                if entry[field.value]==None or entry[field.value]=='':
                    addFlag=False
            if addFlag:
                fullRows.append(entry)
                
        self.catalog=fullRows

    """
    Filters the TSV array to only contain the desired forms of artworks (e.g paintings, portraits, or sculptures)
    """
    def filterForms(self,forms:list):
        self.catalog= [entry for entry in self.catalog if entry[WgaTsv.form.value] in forms]

    def verifyLinkInCatalog(self,link)->int | None:
        "Used to verify that a link is in the catalog, returns it's index if found and -1 if it doesn't exist"
        index=None
        # Linear search through 52,868 items
        for i,entry in enumerate(self.catalog):
            if entry[WgaTsv.url.value]==link:
                index=i
                break
        return index
    
# Testing
if __name__=="__main__":
    parser=WgaParser('catalog.txt')
    fullRows=parser.ensureColumnsNotEmpty([
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
    filtered=parser.filterForms(["painting","portrait"])