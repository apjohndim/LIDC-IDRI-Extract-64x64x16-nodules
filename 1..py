import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import pylidc as pl
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
for pid in path_folders[0:832]:

    #pid = 'LIDC-IDRI-0078' #select a specific folder name with scans
    scans = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).all()
    patID.append(pid)
    
    print ('[INFO] FOUND %4d SCANS' % len(scans))
    for scan in scans:#scan object of this pid
       
       ann = scan.annotations
       vol = scan.to_volume()
       nods = scan.cluster_annotations()
       #anns = nods[0]

       print(len(scan.annotations)) #how many annotations
       print("'[INFO] %s has %d nodules." % (scan, len(nods)))
       
       it = len(nods)
       for nodule in range(0,it):
           #my_id = my_id+1
           x = nods[nodule]
           x = x[0]#grab the first annotation
           print (x.malignancy)  
           slices = x.contour_slice_indices
           place = x.contours_matrix[0]
           xc = place[0]
           yc = place[1]
           g = 0
           slide = slices[int(len(slices)/2)]
           #for slide in slices:
           nodule_count = nodule_count + 1  
           
           for k in range(-8,8):
               vol1 = vol[:,:,slide+k]
               vol1 = vol1[(xc-32):(xc+32),(yc-32):(yc+32)]
               vol1 = (vol1 - np.amin(vol1))/np.amax(vol1)
               vol1 = vol1*255                       
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

       
print ('[INFO] EXTRACTED %4d SCANS' % nodule_count)






#        for i,nod in enumerate(nods):
#            print("Nodule %d has %d annotations." % (i+1, len(nods[i])))
    
   



     
# #%%
#     ann = pl.query(pl.Annotation).filter(pl.Annotation.malignancy > 0).all()
    
#     for ann in ann[:2]:    
#         print ('The malignancy is:', ann.malignancy)
#         X = ann.visualize_in_scan(verbose=True)
    
    #%%
import pylidc as pl
from pylidc.utils import volume_viewer

ann = pl.query(pl.Annotation).first()
vol = ann.scan.to_volume()

padding = 70.0

mask = ann.boolean_mask(pad=padding)
bbox = ann.bbox(pad=padding)

volume_viewer(vol[bbox], mask, ls='-', lw=2, c='r')

