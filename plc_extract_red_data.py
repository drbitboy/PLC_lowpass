"""
Load cell data filter
Cf. https://www.plctalk.net/qanda/showthread.php?t=133372

Input image, data_fixed.png, is modified version of image data.jpg
from Post #18 at the URL above.  This is simpler if you have the
actual data.

Brian T. Carcich, 2022-07-01

"""
import PIL.Image

########################################################################
### Part I:  input the data
### Because we have only the image from the URL, we look for the
### lowest-positioned red-ish pixels in that image, and use the row
### offset from the bottom of the image as a proxy for the measured data
### and the column offset from the left edge of the image as a proxy for
### time
########################################################################

def all_data_by_col(image_path='data.jpg'):
    ### Import image, get width and height, convert to pixels
    imgdata = PIL.Image.open(image_path)
    width,height = wh = imgdata.size
    widths,heights = map(range,wh)
    imgseq = imgdata.getdata()

    ### Loop over columns, get all data
    return [list(zip(*sorted([(height-row,red,green,blue,)
                         for row,(red,green,blue) in
                         [(row,imgseq.getpixel((col,row,)),)
                          for row in heights
                         ]
                        ]
                        )
                    )
                )
            for col in widths
           ]

def red_data(image_path='data_fixed.png'):
    ### Import image, get width and height, convert to pixels
    imgdata = PIL.Image.open(image_path)
    width,height = wh = imgdata.size
    widths,heights = map(range,wh)
    imgseq = imgdata.getdata()

    ### Loop over columns, get lowest contiguous rows that are red
    reddata = [(col
               ,[(height-row,red,)
                 for row,(red,green,blue) in
                 [(row,imgseq.getpixel((col,row,)),)
                  for row in heights
                 ]
                 if red>30 and (red/20)>green and (red/20)>blue and blue<10
                ]
               ,)
               for col in widths
              ]

    ### Average contiguous row values, weighted by redness
    cols = list()
    loads = list()
    for col,data_list in reddata:
      if not data_list: continue
      redsum,redrowsum = 0.0,0.0
      row = data_list[-1][0]
      while data_list:
        nextrow = row+1
        row,red = data_list.pop()
        if row > nextrow: break
        redsum += red
        redrowsum += (red*row)
      cols.append(col)
      loads.append(redrowsum / redsum)

    return cols,loads,image_path

