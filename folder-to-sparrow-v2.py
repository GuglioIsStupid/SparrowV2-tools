import os, sys
from PIL import Image

xmlStr = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

for arg in sys.argv[1:]:
    # Arg is a folder
    foldername = os.path.basename(arg)
    
    # Folder is files 1-#.png
    files = os.listdir(arg)
    files.sort()

    imgList = []
    for i in files:
        if i.endswith(".png"):
            imgList.append(Image.open(arg + "/" + i))
    pngIm = Image.new("RGBA", (0, 0), (0,0,0,0))
    
    # set height based off largest image
    height = 0
    for i in imgList:
        if i.size[1] > height:
            height = i.size[1]
    pngIm = Image.new("RGBA", (len(imgList) * imgList[0].size[0], height), (0,0,0,0))

    curX = 0
    for i in range(len(imgList)):
        im = imgList[i]
        # change width if needed
        if pngIm.size[0] < im.size[0] + curX:
            temp = Image.new("RGBA", (im.size[0] + curX, height), (0,0,0,0))
            temp.paste(pngIm, (0, 0))
            pngIm = temp
        pngIm.paste(im, (curX, 0))
        curX += im.size[0]

    xmlStr += '<TextureAtlas imagePath="' + foldername + '.png">\n'
    for i in range(len(imgList)):
        im = imgList[i]
        xmlStr += '    <SubTexture name="' + os.path.splitext(files[i])[0] + '" x="' + str(im.size[0] * i) + '" y="0" width="' + str(im.size[0]) + '" height="' + str(im.size[1]) + '"/>\n'

    xmlStr += '</TextureAtlas>\n'

    with open(foldername + ".xml", "w") as text_file:
        text_file.write(xmlStr)

    print(foldername + ".png")
    pngIm.save(foldername + ".png")
