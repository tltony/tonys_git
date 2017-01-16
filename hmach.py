
from skimage.transform import rescale
from skimage.io import imread, imsave
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from segment import Dataset
import matplotlib.image  as imagex
# import PIL.Image as Image
from PIL import Image
import os
from openpyxl import load_workbook
import csv
from histmatch import histmatch
import png
from sklearn import preprocessing
import scipy.ndimage as ndimage
import cv2
from skimage.filters import rank
from skimage.morphology import disk



if os.path.exists("bread.csv"):
	os.remove("bread.csv")
	print("File Removed!")

def log(msg, lvl):
    string = ""
    for i in range(lvl):
        string += " "
    string += msg
    print string
    



d = '.'
studies = next(os.walk(os.path.join(d, "train")))[1] + next(os.walk(os.path.join(d, "validate")))[1]    
studies = map(int, studies)    
studies.sort()



studies = range(1,2)
  
for patient_num in studies:
	path = "train/" + str(patient_num)
	d = Dataset(path, "000000")




	try:
		d.load()

		data  = np.zeros((256,256,30,len(d.slices)),  dtype=np.uint16)
		data2 = np.zeros((256,256,30,len(d.slices)),  dtype=np.uint16)



		# for slice_num in range(3, 4 ):
		for slice_num in range(0, len(d.slices) ):


			save_path =  "Output/" + str(patient_num) + "/study/sax_" + str(slice_num+1) + "/"
			if not os.path.exists(save_path):
				os.makedirs(save_path)


			
			add_buf = np.zeros((256,256), dtype =np.uint16)
			# for time_num in range(6, 7):
			for time_num in range(0, 30):




				image_new = d.images[slice_num][time_num]  

				# print d._pixelspacing()
				# print d.images.shape

				scale = 1.6
				(x,y) = d._pixelspacing()



				imgrs = rescale(image_new, (x/scale,y/scale), preserve_range='true')
				imgrs = imgrs.astype(np.uint16)




				### HISTOGRAM MATCH

				href = imread('histref.png')
				# href= imagex.imread("histref.png") 
				hmach = histmatch(imgrs,href)	
				hmach = hmach.astype(np.uint16)

				



				### FILTER/SMOOTH THE IMAGE

				# hmach = cv2.fastNlMeansDenoising(hmach,10)

				# selem = disk(15)
				# hmach = rank.mean_bilateral(hmach, selem=selem, s0=0, s1=500)



				### GENERATE Z-SCORE IMAGE, PER IMAGE

				# std=hmach.std() 
				# mean=hmach.mean() 
				# hmach = (hmach-mean)/std 



				### CREATE THE BOX (256 x 256 FRAME)

				m=256
				n=256
				# result = np.zeros((m,n),  dtype=np.uint16)
				result = 2*np.random.rand(m,n)
				result = result.astype(np.uint16)
				


				### PLACE IMAGE IN BOX

				m_shift= int(np.ceil  (  (m-imgrs.shape[0])/2  ))
				n_shift= int(np.ceil  (  (n-imgrs.shape[1])/2  ))
				result[m_shift : imgrs.shape[0]+m_shift,  n_shift : imgrs.shape[1]+n_shift] = hmach


				### PLACE BOX IN NUMPY ARRAY

				data[:,:,time_num,slice_num] = result


				### KEEP ADDING THE IMAGES (30)

				add_buf = add_buf + result 






			mean_img = add_buf/30
			mean_img.astype(np.float64)
			for time_num in range(0, 30):

				tem = np.zeros((256,256),dtype=np.float64)
				tem= data[:,:,time_num,slice_num]
				tem= tem.astype(np.float64) 
				tem = np.absolute (np.subtract(tem, mean_img))
				tem=tem.astype(np.uint16)

				# tem = preprocessing.scale(tem)

				save_file = save_path + "/" + str(patient_num) + "_" + str(slice_num+1) + "_" +str(time_num+1) + ".png"
				imagex.imsave(save_file, tem, cmap='gray') 
				# imsave('demo.png', tem) 

				data2[:,:,time_num,slice_num] = tem



		# SAVE PATIENT DATA
		np.save("Output/"+ str(patient_num)+ "_dump.npy",data2)

		fields = [str(patient_num),str(imgrs.shape[0]),str(imgrs.shape[1])]
		with open('bread.csv', 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(fields)




	except Exception as e:
		log("***ERROR***: Exception %s thrown by dataset %s" % (str(e), d.name), 0)
		fields=[str(e)]
		with open('bread.csv', 'a') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(fields)


	


	print "DONE"




"""

# plt.figure()
# plt.set_cmap(plt.gray())
# plt.imshow(image_example)
# plt.show()

"""
# fields=[str(patient_num),str(d._pixelspacing()[0]),str(d._pixelspacing()[1]),str(d.images.shape[0]),str(d.images.shape[1]),str(d.images.shape[2]),str(d.images.shape[3])]
