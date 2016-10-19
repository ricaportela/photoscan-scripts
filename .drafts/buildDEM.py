# INIT ENVIRONMENT
import os
import glob
import PhotoScan


print("Build DEM - Started")
doc = PhotoScan.app.document

doc.save("baquinho.psx")

# build DEM

chunk.buildDem(source=PhotoScan.DenseCloudData)

# chunk.buildOrthomosaic()

#proj = PhotoScan.Matrix([[-1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, -1.0, 0.0],  [0.0, 0.0, 0.0, 1.0]])
#chunk.exportDem("/home/ricardo/LearnPath/python/geoprocess-photoscan-cobolman/banquinho/output/teste_DEM.tif", format="tif", dx=1, dy=1, projection=proj)

PhotoScan.app.update()


print("Script finished")
