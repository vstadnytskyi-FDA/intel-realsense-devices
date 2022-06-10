"""
Driver for intel realsense devices. This file contains simple wrappers for functions provided by Intel SDK.
https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python/examples
https://dev.intelrealsense.com/docs/python2

some names of variables and functions come Intel SDK

Currently supports:
Intel LiDAR L515
Intel Depth Camera D435i
"""

import numpy as np 
from time import time, ctime, sleep
import pyrealsense2 as rs
from matplotlib import pyplot as plt
plt.ion()

serial_numbers = ["f1231322"]
config = {}
pipeline = {}
pipeline_wrapper = {}
pipeline_profile = {}
device = {}

for serial_number in serial_numbers:
# Create a context object. This object owns the handles to all connected realsense devices
    sn = serial_number
    pipeline[sn] = rs.pipeline()

    # Configure streams
    config[sn] = rs.config()
    config[sn].enable_device(sn)
    pipeline_wrapper[sn] = rs.pipeline_wrapper(pipeline[sn])
    pipeline_profile[sn] = config[sn].resolve(pipeline_wrapper[sn])
    device[sn] = pipeline_profile[sn].get_device()
    device_serial_number = str(device[sn].get_info(rs.camera_info.serial_number))
    device_product_line = str(device[sn].get_info(rs.camera_info.product_line))
    print(device_product_line,device_serial_number)
    
    config[sn].enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    if device_product_line == 'L500':
        config[sn].enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config[sn].enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline[sn].start(config[sn])


serial_number = 'f1231322' 
frames = pipeline[serial_number].wait_for_frames()
depth_frame = frames.get_depth_frame()
color_frame = frames.get_color_frame()

# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())

#to plot data

plt.figure(figsize = (24,12))
plt.subplot(121)
plt.imshow(depth_image)
plt.axvline(225)
plt.axhline(200)
plt.axhline(200)

plt.subplot(122)
plt.imshow(color_image)
t = time()
plt.figure()
plt.plot(depth_image[:350,220:225])

t=time()

def save_to(color_image,depth_image, t,filename):
    # to save data to a hard drive
    from ubcs_auxiliary.save_load_object import save_to_file
    save_to_file(filename,{'color':color_image,'depth':depth_image,'time':t})

filename = r'C:\Users\AR-VR lab W1\Documents\Valentyn\data\intel Lidar L515\scratch_lidar_images.txt'
save_to(color_image,depth_image, t,filename)