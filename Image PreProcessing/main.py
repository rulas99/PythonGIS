from glob import glob
from functions import *

f=glob("/Users/rauldelarosa/Desktop/Octavo/PR2/act4/Img_L8/*.TIF") #Ruta de la carpeta que contiene tus imagenes L8 (separadas por banda)
rutmtl=glob("/Users/rauldelarosa/Desktop/Octavo/PR2/act4/Img_L8/*_MTL.txt")[0] #Ruta del arhivo mtl correspondiente a las imagenes anteriores

for i in f:
    b=i[:-4].split("_")[-1]
        
    img=readImgAsMatrix(i)
    dat=img[0]
    img2=img[1]
    
    del img
    
    mtl=readMtl(rutmtl)

    try:
        rad=cofRadiance(mtl,b[1:])
        ref=cofReflectance(mtl,b[1:])
        
        datRad=toRadiance(dat,rad)
        datRef=toReflectance(dat,ref)

        saveImg("/Users/rauldelarosa/Desktop/Octavo/PR2/act4/PreProcesadas/Rad_{}".format(b),datRad,img2)
        saveImg("/Users/rauldelarosa/Desktop/Octavo/PR2/act4/PreProcesadas/Ref_{}.TIF".format(b),datRef,img2)

        del datRef, dat, img2 ,datRad
    except:
        pass
