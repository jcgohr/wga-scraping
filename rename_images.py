# This script fixes an issue where two files will have the same name but with different cases
# The best example of this is images/BASCHENIS, Evaristo\Still-(L orl)ife with Musical Instruments.jpg
# On linux this issue is is non-existent as the difference in casing makes them unique files
# If the operating system does not take case into account these will be considered the same file
# To fix this issue we rename the duplicates
import os


IMG_DIR="../../images"
for directory in os.listdir(IMG_DIR):
    images=os.listdir(os.path.join(IMG_DIR,directory))
    lower_case_images=[image.lower() for image in images]
    # A dictionary used to keep track of multiple uncased duplicates
    duplicates_dict={}
    for i in range(len(lower_case_images)):
        image=lower_case_images.pop(0)
        # This if statement checks that after popping the head of the list its still in the list
        if image in lower_case_images:
            dupe_idx=lower_case_images.index(image)
            image_path=os.path.join(IMG_DIR,directory,images[dupe_idx])
            print(f"uncased duplicate found at {image_path}")
            #Rename the file with a (d) for duplicate which makes them different
            os.rename(
                image_path,
                # Remove .jpg extension and add uncased duplicate identifier
                image_path[:-4]+f" (d{duplicates_dict[image] if image in duplicates_dict else ''}).jpg"                
            )
            # Update duplicate dict
            if image not in duplicates_dict:
                duplicates_dict[image]=1
            else:
                duplicates_dict[image]+=1
