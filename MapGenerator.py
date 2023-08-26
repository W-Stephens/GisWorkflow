from skimage.measure import block_reduce
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import sys
import os
import contextily as cx
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import matplotlib.image as mpimg


from utilities import get_basins

# TIF FILE GET AND ERROR CHECK




tif_get = input("Please enter the path to the .tif file: ")
assert os.path.exists(tif_get), "Could not find the file at, "+str(tif_get)

    # READ TIF FILE IN

ras = rasterio.open(tif_get)
arr = ras.read(1)

    # SHRINKING THE ARRAY TO SPEED IT UP

arrsm = block_reduce(arr, (40, 40), np.nanmean)
arrsm = np.where(arrsm==0, np.nan, arrsm)

    # GETTING BASIN BOUNDS

basin_get = input("Please enter the basin code: ")

basins = get_basins()
basinofinterest = basins[basins.abbreviation == basin_get ]
w, s, e, n = basinofinterest.to_crs('EPSG:3857').bounds.values.flatten()

    # GETTING BACKGROUND IMAGE IN UTM PROJECTION

img, ext = cx.bounds2img(w, s, e, n, zoom=10)
warped_img, warped_ext = cx.warp_tiles(img, ext, "EPSG:32611")

    # GETTING THE RASTER EXTENT IN THE PROPER ORDER FOR plt.imshow KEYWORD EXTENT

b = ras.bounds
rasextent = b.left, b.right, b.bottom, b.top

    # PLOTTING

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.imshow(warped_img, extent=warped_ext)
ax.imshow(arrsm, extent=rasextent, vmax=2, cmap='YlGnBu')
basinofinterest.plot(ax=ax, facecolor='none', linewidth=2, edgecolor='r')

bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="k", lw=2)


ax.set_title(str(basinofinterest.name.to_string(index=False)))

logo = mpimg.imread(r'C:\Users\Gamer\Desktop\Code\ASOLogo_withText.png')
imagebox = OffsetImage(logo, zoom=0.04)

ab = AnnotationBbox(imagebox, xy = (0.83, 0.82),
    xycoords='axes fraction',
    boxcoords="offset points")

ax.add_artist(ab)

plt.savefig(str(basinofinterest.name.to_string(index=False)) + '.pdf', dpi=None, facecolor='w', edgecolor='w', orientation='portrait', transparent=False, pad_inches=0.1)

plt.show()
