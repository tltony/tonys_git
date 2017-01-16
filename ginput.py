# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 12:38:18 2016

@author: bmi
"""

#!/usr/bin/env python
# -*- noplot -*-

from __future__ import print_function
"""
This script must be run interactively using a backend that has a
graphical user interface (for example, using GTKAgg backend, but not
PS backend).

"""
import time
import numpy as np
import matplotlib
matplotlib.use('QT4Agg')
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import csv
import os
import cv2
import re
import shutil

filename = "patient.csv"



"""
TODO

import sys

sys.path.append('/usr/local/lib/python2.7/dist-packages')


#if __name__ == "__main__":
#    random.seed()
## write function
#    ginput()
st = sys.argv[1]


"""
def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()

# Define a nice function of distance from individual pts
def dist(p1, p2):
    return (np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2))

def draw_circle(img, center, r, color, thickness):
    (x, y) = center
    x, y = int(np.round(x)), int(np.round(y))
    r = int(np.round(r))
    cv2.circle(img, center=(x, y), radius=r, color=color, thickness=thickness)


    
d = '.'
studies = next(os.walk(os.path.join(d, "train")))[1]
studies = map(int, studies)    
studies.sort()


for st in studies:
    #Patient number till work of annotation done to be skipped
    if st <= 0:
        continue
    outputfolder = os.path.join(d, "output")
    if not os.path.exists(outputfolder):
        os.mkdir(outputfolder)
    if st >= 43 and st <=43:
        full_path = os.path.join(d, "train", str(st))
        while True:
            subdirs = next(os.walk(full_path))[1]
            if len(subdirs) == 1:
                full_path = os.path.join(full_path, subdirs[0])
            else:
                break
        slices = []
        for sb in subdirs:
            m = re.match("sax_(\d+)", sb)
            if m is not None:
                slices.append(int(m.group(1)))        
        slices.sort()    
#        pat = "Preprocessing Patient ID %d" % str(st)
#        print 'Patient ID {}'.format()
#        file_full_paths = []      
        csvfile = '/'+str(st) + '_' + filename
        filecsv = outputfolder + csvfile
        if os.path.exists(filecsv):
            os.remove(filecsv)
        for s in slices:
            files = next(os.walk(os.path.join(full_path, "sax_%d" % s)))[2]
            files = sorted(files, key = lambda x: int(x.split("_")[2].split('.')[0]))
            roi_folder = os.path.join(full_path, "sax_%d" % s,'roi')
            if os.path.exists(roi_folder):
                shutil.rmtree(roi_folder)
            os.mkdir(roi_folder)            
            for f in files:
                path = os.path.join(full_path, "sax_%d" % s,f)
#                file_full_paths.append(f)           
#                print('file {}.'.format(path))
                img=mpimg.imread(path)
                h=plt.figure()
                plt.clf()
#                plt.axis([0.0, 1., 0.0, 1.])
#                plt.setp(plt.gca(), autoscale_on=True)
                figManager = plt.get_current_fig_manager()
                figManager.window.showMaximized()
                # figManager.full_screen_toggle()
                # figManager.window.state('iconic')
                imgplot = plt.imshow(img, cmap = 'gray')
               
                tellme( 'Patient ID: {0} Slice: {1} TP: {2}. Click to begin'.format(st,s,f))
                plt.waitforbuttonpress()
                happy = False
                while not happy:
                    pts = []
                    while len(pts) < 3:
                        tellme('Select 3 points with mouse - circle center, inner and outer radius')
                        pts = plt.ginput(3, timeout=-1)
                        if len(pts) < 3:
                            tellme('Too few points, starting over')
                            time.sleep(1)  # Wait a second
                        else:
                            center = pts[0]
                            inner_circle_cordn = pts[1]
                            ext_circle_cordn = pts[2]
                            #Calculate inner radius
                            inner_radius = dist(center, inner_circle_cordn)
                            outer_radius = dist(center, ext_circle_cordn)                            
                            pts = np.asarray(pts)
#                   ##draw two circles 
                    circle1 = plt.Circle(center, inner_radius, color='b', fill=False)
                    circle2 = plt.Circle(center, outer_radius, color='r', fill=False)
                    ax = plt.gca()
                    ax.add_artist(circle1)
                    ax.add_artist(circle2)                    
                    tellme('Happy? Press Enter for YES or Mouse click for NO')
                    happy = plt.waitforbuttonpress()
                #     Get rid of fill
                    if not happy:
                        circle1.remove()
                        circle2.remove()
                    else:
                        fields = [center[0],center[1],inner_circle_cordn[0],inner_circle_cordn[1] 
                        ,ext_circle_cordn[0],ext_circle_cordn[1],inner_radius,outer_radius]
                        with open(filecsv, 'a') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(fields)
                        tmp = np.zeros_like(img[:,:,0])
                        draw_circle(tmp, center, inner_radius, 1, -1)
                        ROI_img = roi_folder+'/'+f
                        mpimg.imsave(ROI_img, tmp * img[:,:,0], cmap='gray') 
                        plt.close(h)

###################################################
## Now do a zoom
###################################################
#tellme('Now do a nested zoom, click to begin')
#plt.waitforbuttonpress()
#
#happy = False
#while not happy:
#    tellme('Select two corners of zoom, middle mouse button to finish')
#    pts = np.asarray(plt.ginput(2, timeout=-1))
#
#    happy = len(pts) < 2
#    if happy:
#        break
#
#    pts = np.sort(pts, axis=0)
#    plt.axis(pts.T.ravel())
#
#tellme('All Done!')
#plt.show()