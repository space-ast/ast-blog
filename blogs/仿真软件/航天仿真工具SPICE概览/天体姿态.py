import spiceypy as sp
import numpy as np

# 加载所需内核
sp.furnsh('kernels/lsk/naif0012.tls')
sp.furnsh('kernels/pck/pck00011.tpc')

# 设置参数
from_frame = 'IAU_EARTH'  # 地球固定坐标系
to_frame = 'J2000'   # 参考坐标系

# 时间转换
date_str = '2013-01-01T12:00:00'
et = sp.utc2et(date_str)

# 获取姿态矩阵（方向余弦矩阵）
rot_mat = sp.pxform(from_frame, to_frame, et)
print(type(rot_mat))

print(f"{date_str}时，{from_frame}到{to_frame}的方向余弦矩阵:\n{np.array(rot_mat).reshape(3, 3)}")

# 计算欧拉角（ZYX顺序）
euler_angles = sp.m2eul(np.array(rot_mat).reshape(3, 3), 3, 2, 1)
print(f"对应的欧拉角(ZYX, 度): {[angle * 180 / np.pi for angle in euler_angles]}")

# 卸载内核
sp.kclear()