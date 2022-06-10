# Intel RealSense Lidar L515 Example
# In this example, we create multiple pipelines to take advantage of higher acquisition rate for gyroscope and accelerator

#NOTE, MAKE SURE TO CHANGE SERIAL NUMBER

SERIAL_NUMBER = 'f1231322'

import pyrealsense2 as rs
import numpy as np
import time
from PIL import Image as im
from matplotlib import pyplot as plt
import subprocess
def initialize_camera():
    ctx = rs.context()
    devices = ctx.query_devices()
    dev = None
    for device in devices:
        print(' ----- Available devices ----- ')
        print('  Device PID: ',  device.get_info(rs.camera_info.product_id))
        print('  Device name: ',  device.get_info(rs.camera_info.name))
        print('  Serial number: ',  device.get_info(rs.camera_info.serial_number))
        print('  Firmware version: ',  device.get_info(rs.camera_info.firmware_version))
        print('  USB: ',  device.get_info(rs.camera_info.usb_type_descriptor))
        serial=device.get_info(rs.camera_info.serial_number)
        if serial == SERIAL_NUMBER:
            dev = device
        else:
            print('device not found')
 
    serial=dev.get_info(rs.camera_info.serial_number)
    # start the frames pipeline
    pipeline = rs.pipeline()
    conf = rs.config()
    conf.enable_device(serial)   #test of enable device
    profile = pipeline.start(conf)
    print ('camera init complete')
    time.sleep(2)
    return pipeline, profile
pipeline,profile = initialize_camera()
stream_list =profile.get_streams()
for i in stream_list:
    print(f'stream {i}')
try:
    for i in range(10):
        f = pipeline.wait_for_frames()
        accel = (f[3].as_motion_frame().get_motion_data())
        gyro =  (f[4].as_motion_frame().get_motion_data())
        color = f.get_color_frame()
        infrared = f.get_infrared_frame()
        depth = f.get_depth_frame()
        dist = (depth.get_distance(240, 320))
        color_img = np.asanyarray(color.get_data())
        ir_img = np.asanyarray(infrared.get_data())
        depth_img = np.asanyarray(depth.get_data())
        print('--- --- --- --- --- ---')
        print("accelerometer: ", accel)
        print("gyro: ", gyro)
        print('gyro frame #: ',f[3].get_frame_number())
        print('distance: ', dist)
        print('dist frame #: ',f[0].get_frame_number())
        print('mean color: ', color_img.mean())
        print('mean depth: ', depth_img.mean())
        print('mean infrared: ', ir_img.mean())
        #print('color: ', (col[400,400]))
        #print(data)
        #print('col array shape',col.shape)
        #print('infrared: ', (IRcol[240,320]))
        #time.sleep(0)
        #subprocess.check_call('cls',shell=True)
finally:
    pass #p.stop()


plt.ion() #interactive on - turns on interactive mode for matplotlib plots. Otherwise you need to have plt.show() command

plt.figure(figsize = (8,4))
plt.subplot(131)
plt.imshow(depth_img)
plt.title('depth_image')

plt.subplot(132)
plt.imshow(color_img)
plt.title('color image')

plt.subplot(133)
plt.imshow(ir_img)
plt.title('infrared image')

# Orderly exit
print("Stopping the pipeline...")
pipeline.stop()