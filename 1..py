import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import pylidc as pl #!!!!!!!!!!!!! YOU NEED TO INSTALL IT; pip install pylidc
import os 
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from imutils import paths
import matplotlib.pyplot as plt
import random
import cv2
from PIL import Image
patID = []

#%%
scans = pl.query(pl.Scan).filter(pl.Scan.slice_thickness <= 5,
                                 pl.Scan.pixel_spacing <= 5) #load all scans in object scan
print(scans.count()) #print how many scans have the particular chracterisics: slice_thickness and pixel_spacing

path = 'J:\\PHD + MSC DATASETS\\Datasets\\LIDC DATABASE\\LIDC-IDRI\\'
path_folders = os.listdir(path)

path2 = 'J:\\PHD + MSC DATASETS\\Datasets\\LIDC DATABASE\\3d\\'
nodule_count = 0
my_id = 1
for pid in path_folders[0:832]: #adjust according to the number of folders you downloaded

    scans = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).all() #obtain the scans
    patID.append(pid) #useless
    
    print ('[INFO] FOUND %4d SCANS' % len(scans))
    for scan in scans:#scan object of this pid
       
       ann = scan.annotations
       vol = scan.to_volume() #obtain the volume numpy array
       nods = scan.cluster_annotations() #obtin the nodules object from this scan
       #anns = nods[0]

       print(len(scan.annotations)) #how many annotations
       print("'[INFO] %s has %d nodules." % (scan, len(nods)))
       
       it = len(nods) #define how many nodules. nods is not iterable, be carefull
       for nodule in range(0,it):
           #my_id = my_id+1
           x = nods[nodule] #get only the first annotation
           x = x[0]#grab the first annotation
           print (x.malignancy)  
           slices = x.contour_slice_indices #in which slices the nodule appears
           place = x.contours_matrix[0] #grab a relative ccordinate
           xc = place[0] #
           yc = place[1] #
           g = 0
           slide = slices[int(len(slices)/2)] #go to the mean slice
           #for slide in slices:
           nodule_count = nodule_count + 1  
           
           for k in range(-8,8): #I extract 16 slices
               vol1 = vol[:,:,slide+k] #get the image of the particular slice
               vol1 = vol1[(xc-32):(xc+32),(yc-32):(yc+32)] #for 64x64. 
               vol1 = (vol1 - np.amin(vol1))/np.amax(vol1) # adjust the pixel values to 0,1
               vol1 = vol1*255 #adjust to 0,255                      
               im = Image.fromarray(vol1)
               im = im.convert("L")                   
               if x.malignancy < 3:
                   lab = 'benign'
                #name = path + pid + '\\' + lab + str(g) + str('Series:') + str(my_id) + '.tif'
                   im.save(path2 + str('Nod_') + str(nodule_count) + 'Slice_' + str(k+5) + 'Patient number_' + str(my_id)+ lab + '.tif')
               else: 
                   lab='malignant'
                   im.save(path2 + str('Nod_') + str(nodule_count) + 'Slice_' + str(k+5) + 'Patient number_' + str(my_id)+ lab + '.tif')
                                             
               g = g + 1
           my_id = my_id + 1     

       
print ('[INFO] EXTRACTED %4d NODULES' % nodule_count)



