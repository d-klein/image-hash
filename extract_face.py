import numpy as np
import matplotlib.pyplot as plt

from skimage import data
from skimage.feature import match_template

import Image

needle_rgb = Image.load("90a_scan.png")
needle = Image.rgb2gray(needle_rgb)

haystack_rgb = Image.load("90a_camera.jpg")
haystack = Image.rgb2gray(haystack_rgb)

result = match_template(haystack, needle)
ij = np.unravel_index(np.argmax(result), result.shape)
x, y = ij[::-1]

fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, figsize=(8, 3))

ax1.imshow(needle)
ax1.set_axis_off()
ax1.set_title('template')

ax2.imshow(haystack)
ax2.set_axis_off()
ax2.set_title('image')
# highlight matched region
hcoin, wcoin = needle.shape
rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
ax2.add_patch(rect)

ax3.imshow(result)
ax3.set_axis_off()
ax3.set_title('`match_template`\nresult')
# highlight matched region
ax3.autoscale(False)
ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

plt.show()

