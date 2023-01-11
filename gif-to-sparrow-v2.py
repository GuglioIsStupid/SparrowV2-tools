import os, sys
# this tool can be used to convert gifs to adobe sparrow v2
# import an image tool
from PIL import Image

xmlStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
# example is <SubTexture name="anim0000" x="0" y="0" width="0" height="0" frameX="0" frameY="0" frameWidth="0" frameHeight="0"/>

# for all in arguments
for arg in sys.argv[1:]:
    # get the filename
    filename = os.path.basename(arg)
    # get the name without extension
    name = os.path.splitext(filename)[0]
    # open the image
    im = Image.open(arg)

    # since it is a gif, we need to go through all the frames
    gifFrameList = []
    pngIm = Image.new("RGBA", (im.size[0]*im.n_frames, im.size[1]), (0,0,0,0))
    for i in range(im.n_frames):
        # add the frames x, y, width, and height to the table
        im.seek(i)
        if i == 0:
            gifFrameList.append([0, 0, im.size[0], im.size[1]])
        else:
            gifFrameList.append([gifFrameList[i-1][0]+gifFrameList[i-1][2], 0, im.size[0], im.size[1]])
        # add the frame to the png
        pngIm.paste(im, (gifFrameList[i][0], gifFrameList[i][1]))
    
    # create the xml file
    xmlStr += '<TextureAtlas imagePath="' + name + '.png">\n'
    for i in range(im.n_frames):
        xmlStr += '\t<SubTexture name="' + name + str(i).zfill(4) + '" x="' + str(gifFrameList[i][0]) + '" y="' + str(gifFrameList[i][1]) + '" width="' + str(gifFrameList[i][2]) + '" height="' + str(gifFrameList[i][3]) + '" frameX="0" frameY="0" frameWidth="' + str(gifFrameList[i][2]) + '" frameHeight="' + str(gifFrameList[i][3]) + '"/>\n'

    xmlStr += '</TextureAtlas>\n'
        
    # save the png and xml
    with open(name + ".xml", "w") as text_file:
        text_file.write(xmlStr)
    pngIm.save(name + ".png")
