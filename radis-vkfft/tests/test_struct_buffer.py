
import sys
sys.path.append('..')
import os

from vulkan_compute_lib import GPUApplication, GPUArray, GPUStruct, GPUBuffer
import numpy as np
from scipy.fft import next_fast_len
from numpy.fft import rfftfreq
from numpy.random import rand, randint, seed
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from ctypes import Structure, c_float, c_int, sizeof, cast, POINTER
from time import perf_counter
import vulkan as vk
import sys

c_float_arr_16 = c_float * 16
class initData_t(Structure):
    _fields_ = [
        ("v_min", c_float),
        ("dv", c_float),
        ("N_v", c_int),
        ("N_v_FT", c_int),
        ("N_x_FT", c_int),
        ("dxG", c_float),
        ("dxL", c_float),
        ("N_lines", c_int),
        ("N_coll", c_int),
        ("log_c2Mm", c_float_arr_16),
    ]






# Init Vulkan
shader_path = os.path.dirname(__file__)
app = GPUApplication(deviceID=0, path=shader_path)
app.print_memory_properties()

initData = initData_t()

buf = GPUBuffer(sizeof(initData_t), app=app)
arr = np.zeros(sizeof(initData_t), dtype=np.uint8)
ptr = cast(arr.ctypes.data, POINTER(initData_t)).contents

buf.initStagingBuffer()
initData = buf.getHostStructPtr(initData_t)
initData.N_v = 123
initData.N_v_FT = 456
initData.N_x_FT = 789

buf.copyFromBuffer(arr)
print(arr.view(np.int32))

sys.exit()


copy_region = vk.VkBufferCopy(srcOffset=0, dstOffset=0, size=buf_dev._bufferSize)
app.oneTimeCommand(vk.vkCmdCopyBuffer,
                   srcBuffer=buf_dev._buffer,
                   dstBuffer=buf_dev2._buffer,
                   regionCount=1,
                   pRegions=[copy_region],
                   )


N = 1024*1024
arr = np.arange(0, N, 2, dtype=np.int32)
arr2 = np.zeros(arr.size, dtype=np.int32)
arr3 = np.zeros(arr.size, dtype=np.int32)

print('arr.nbytes', arr.nbytes)

buf_dev = GPUBuffer(arr.nbytes, app=app)
buf_dev.initStagingBuffer(32*1024*1024)

buf_dev2 = GPUBuffer(arr.nbytes, app=app)
buf_dev2.initStagingBuffer(32*1024*1024)


print('Copying data... ')
t0 = perf_counter()
buf_dev.copyToBuffer(arr)
t1 = perf_counter()
buf_dev.copyFromBuffer(arr2)
##t2 = perf_counter()
print(arr2)
print('copy_to:  ', (t1-t0)*1000)

copy_region = vk.VkBufferCopy(srcOffset=0, dstOffset=0, size=buf_dev._bufferSize)
app.oneTimeCommand(vk.vkCmdCopyBuffer,
                   srcBuffer=buf_dev._buffer,
                   dstBuffer=buf_dev2._buffer,
                   regionCount=1,
                   pRegions=[copy_region],
                   )

t3 = perf_counter()
buf_dev2.copyFromBuffer(arr3)
t4 = perf_counter()
print(arr3)
print('copy_from:', (t4-t3)*1000)

print('Done!')
