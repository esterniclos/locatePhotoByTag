# Tested in python 2.7
# 
# Ester Niclos Ferreras
# 9 mayo 2019

import sys, os
import PIL
from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import TAGS




def printUsage ():
	print ("Usage: " + sys.argv[0] + " sourceFolder listtagsfile" )
	if (len(sys.argv) < 3):
			print ("Missing arguments")
			exit (1)


printUsage()

folderList = []
folderList.append (sys.argv[1])
tagslist = sys.argv[2]

f = open (tagslist,'r')
tags = f.readlines()
tags = map(lambda s: s.strip(), tags)
f.close()
print ("Looking for tags" + str(tags))

def isPhotoTagged (photo,tags):
	if ("\\.mp4" in photo):
		return False
		
	isTagged = (isXMPTagged (photo, tags) or 
		(isExifTagged(photo,tags)))
	# exit (1)
	return isTagged

def isXMPTagged (photo, tags):
	fd = open(photo)
	d= fd.read()
	fd.close()
	
	xmp_start = d.find('<x:xmpmeta')
	xmp_end = d.find('</x:xmpmeta')
	xmp_str = d[xmp_start:xmp_end+12]
	# print(xmp_str)
	for tag in tags:
		if (tag in xmp_str):
			print ( "   XMP " + photo + " - "  +tag)
			return True
	return False
	
def isIPTCTagged (photo, tags):
	return False
	
	

def isExifTagged (photo, tags):

	exifData = {}
	try: 
		img = PIL.Image.open(photo)
	except:
		return False # It is not even an image
	exif_data = img._getexif()
	exifDataRaw = img._getexif()
	if (exifDataRaw == None):
		return False
	for k, value in exifDataRaw.items():
		decodedTag = ExifTags.TAGS.get(k, k)
		for tag in tags:
			if (tag in str(value)):
				print ( "   EXIF " + photo + " - "  +tag)
				return True
		exifData[decodedTag] = value
	# print (exifData) # Print when nothing is 
	return False
	

lPhotoTagged = []

while (len(folderList) > 0):
	folder = folderList[0]
	print ("\nOpen " + folder)
	for item in os.listdir(folder):
		fullPath=folder+"/"+ item
		# If it is a folder, save in list for later:
		if os.path.isdir(fullPath) :
			folderList.append (fullPath)
		else:
			if (isPhotoTagged(fullPath, tags)):
				lPhotoTagged.append (str(fullPath))
				print ("Total photo tagged: " + str(len(lPhotoTagged)))
	del folderList [0]

# Export files found
fn = sys.argv[0] + "_result.txt"
writer = open(fn, "w")
for photoTagged in lPhotoTagged:
        writer.write(str(photoTagged)+ "\n")
writer.close()


print ("List of matching files can be retrieved from ")
print (fn)
