# INIT ENVIRONMENT
import os
import glob
import PhotoScan


print("Alinhando Fotos - Started")
doc = PhotoScan.app.document

# align photos
chunk.matchPhotos(accuracy=PhotoScan.Accuracy.HighAccuracy, preselection=PhotoScan.Preselection.GenericPreselection, filter_mask=False, keypoint_limit=40000, tiepoint_limit=10000)
chunk.alignCameras()
chunk.optimizeCameras()
PhotoScan.app.update()
doc.save("baquinho.psz")
print("Script finished")
