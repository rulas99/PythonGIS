from glob import glob
from functions import *

f=glob("Img_L8/*.TIF") #Ruta de la carpeta que contiene tus imagenes L8 (separadas por banda)
rutmtl=glob("Img_L8/*_MTL.txt")[0] #Ruta del arhivo mtl correspondiente a las imagenes anteriores

for i in f:
    b=i[:-4].split("_")[-1]
    
    img=readImgAsMatrix(i)
    dat=img[0]
    img2=img[1]
    
    del img
    
    mtl=readMtl(rutmtl)
    print(b[1:])
    rad=cofRadiance(mtl,b[1:])
    ref=cofReflectance(mtl,b[1:])
    
    datRad=toRadiance(dat,rad)
    datRef=toReflectance(dat,ref)
    
    saveImg("PreProcesadas/Rad_{}".format(b),datRad,img2)
    saveImg("PreProcesadas/Ref_{}".format(b),datRef,img2)

    del datRad, datRef, dat, img2