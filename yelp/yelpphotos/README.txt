CONTENTS
0 DESCRIPTION
1 SYSTEM REQUIREMENTS
2 USAGE
3 DATASET SPECIFICS

0 DESCRIPTION

This folder contains code to extract certain photos from the yelp
photo set. The filter criteria is that all photos with non food
labels and no captions are filtered out using the photo.json file.
The resulting filtered output can then be used in conjunction with
the actual photos with ID names to actually display the photos.
This is all done in the photo_processing.py file.

1 SYSTEM REQUIREMENTS

Python version 3.4 and above needed to use the pathlib package. 

2 USAGE
To limit the size of the output data to only a single
business_id the variable 'business' within
photo_processing.py must be set to the business_id.
Or if you want to select all filtered businesses then set the
variable 'business' to the string "all".
Note a file photos.json containing all json data of the photos
and a folder named photos containing the actual jpg photos with
each photo named to a specific photo_id should be placed in the same directory as this folder.
Calling the method copy_photos() will ouput all food realated photos in the state Arizona contained in the a folder named photos in the same directory as this file. This photos folder should contain the yelp photo dataset which will not be uploaded to gitlab in htis repositry as it is too large, but it is required by you the user to place it there.

3 DATASET SPECIFICS
To use the code in the photo_processing.py it is assumedd that the yelp dataset is already imported into a neo4j database. The code was tested with the datset imported using the following repositry: 
https://github.com/DavidBakerEffendi/neo4j-yelp.
