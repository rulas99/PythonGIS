import rasterio
import numpy as np

def readMtl(rutmtl):
    with open(rutmtl) as mtl:
        l=mtl.readlines()
    return l

def cofRadiance(mtl,rut):
    for i in mtl:
        print()
        if i.find("RADIANCE_MULT_BAND_{}".format(rut))!=-1:
            radMult = float(i.split("=")[1])

        if i.find("RADIANCE_ADD_BAND_{}".format(rut))!=-1:
            radAdd = float(i.split("=")[1])
    
    return {"radAdd":radAdd,"radMult":radMult}

def cofReflectance(mtl,rut):
    for i in mtl:
        if i.find("REFLECTANCE_MULT_BAND_{}".format(rut))!=-1:
            refMult = float(i.split("=")[1])

        if i.find("REFLECTANCE_ADD_BAND_{}".format(rut))!=-1:
            refAdd = float(i.split("=")[1])
    
    return {"refAdd":refAdd,"refMult":refMult}

def readImgAsMatrix(rutImg):
    img2=rasterio.open(rutImg)
    dat=img2.read()[0]
    dat=np.where(dat!=0,dat,np.nan)
    
    return dat,img2

def saveImg(rut,res,img2):
    with rasterio.open(
    rut,
    'w',
    driver='GTiff',
    height=res.shape[0],
    width=res.shape[1],
    count=1,
    dtype=res.dtype,
    crs=img2.crs,
    transform=img2.transform,
    ) as dst:
        dst.write(res, 1)

def toRadiance(dat,rad):
    return dat*rad["radMult"]+rad["radAdd"]

def toReflectance(dat,ref):
    return dat*ref["refMult"]+ref["refAdd"]