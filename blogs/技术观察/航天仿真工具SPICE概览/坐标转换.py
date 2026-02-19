import spiceypy as sp
import numpy as np

# 加载所需内核
sp.furnsh('kernels/lsk/naif0012.tls')
sp.furnsh('kernels/pck/pck00011.tpc')

# 设置参数
from_frame = 'IAU_EARTH'  # 源坐标系
to_frame = 'J2000'        # 目标坐标系

# 时间转换
date_str = '2013-01-01T12:00:00'
et = sp.utc2et(date_str)

# 获取坐标转换矩阵(6 x 6)
rot_mat = sp.sxform(from_frame, to_frame, et)

# 坐标转换
state_ecf = [-1000.0, 2000.0, 5000.0, 1.0, -0.5, 2.0]  # x,y,z, vx,vy,vz
state_j2000 = rot_mat @ state_ecf

print(f"ecf坐标: {state_ecf}")
print(f"J2000坐标: {state_j2000}")