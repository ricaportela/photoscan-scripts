# INIT ENVIRONMENT
import os
import glob
import PhotoScan

print("Started...Add Photos")
doc = PhotoScan.app.document
# doc.remove(doc.chunks)
chunk = doc.addChunk()
chunk.label = "Banquinho"
# Define: Source images
aerialimagespattern = ("/home/ricardo/LearnPath/python/geoprocess-photoscan-cobolman/banquinho/source_images/*.JPG")
aerialimagefiles = glob.glob(aerialimagespattern)
chunk.addPhotos(aerialimagefiles)
PhotoScan.app.update()

# save
doc.save("baquinho.psz")
PhotoScan.app.update()
print("End...Add Photos")
