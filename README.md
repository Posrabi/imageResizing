# ImageResizing
Uses dynamic programming to resize images base on their "activity level". When resizing, pixels with that is less interesting, that is rougly the same colour to the surrounding pixels, will be deleted. Only "interesting" region with lots of activity will be left. Implemented this by deleting the seam with the lowest total energy level of the picture.
Sample input file surfer.jpg, output file surfer-resize-{number of seams remove}.jpg
To clearly see the difference, open the two image fullscreen and switch back and forth from them using the tab switcher.
