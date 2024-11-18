# This script fixes an issue where two files will have the same name but with different cases
# The best example of this is images/BASCHENIS, Evaristo\Still-(L orl)ife with Musical Instruments.jpg
# On linux this issue is is non-existent as the difference in casing makes them unique files
# If the operating system does not take case into account these will be considered the same file
# To fix this issue we rename the duplicates
from WgaFetcher import rename_uncased_duplicates
import json
import sys
import os

metadata_path=sys.argv[1]

FP="file_path"

with open(metadata_path,encoding="utf-8") as metadata_file:
    metadata=json.load(metadata_file)

base_dir_grouping={}

for key in metadata:
    image_dir=os.path.dirname(metadata[key][FP])
    if image_dir not in base_dir_grouping:
        base_dir_grouping[image_dir]=[key]
    else:
        base_dir_grouping[image_dir]+=key
    
modified_files=[]
for directory in base_dir_grouping:
    renamed=rename_uncased_duplicates(directory,rename=True)
    if renamed:
        modified_files.append(renamed)
        
for renames in modified_files:
    for key,value in renames.items():
        for id in metadata:
            if metadata[id][FP]==value:
                metadata[id][FP]=key
        
with open(metadata_path,"w",encoding="utf-8") as metadata_file:
    metadata_file.write(json.dumps(metadata,indent=4,ensure_ascii=False))