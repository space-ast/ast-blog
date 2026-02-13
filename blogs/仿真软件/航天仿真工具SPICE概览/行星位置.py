import spiceypy as sp

# 加载所需的内核文件
sp.furnsh([
    'kernels/lsk/naif0012.tls',   #  闰秒数据内核(LSK)
    'kernels/spk/de430.bsp'       #  行星DE星历数据内核(SPK)
])     

# 设置时间
target = 'Mars Barycenter'          #  目标天体(火星系质心，与火星质心很接近)
observer = 'Earth'                  #  观测者(地球)
reference_frame = 'J2000'           #  参考坐标系(J2000)
aberration_correction = 'LT+S'      #  光行差修正项(aberration correction)

# 转换时间为ET(Ephemeris Time)
date_str = 'July 4, 2003 11:00 AM PST'
et = sp.str2et(date_str)

# 获取火星相对于地球的位置
position, light_time = sp.spkpos(target, et, reference_frame, aberration_correction, observer)

print(f"{date_str}时\n火星系质心相对于地球的位置(km): {position}")
print(f"光行时(s): {light_time}")

# 卸载内核文件
sp.kclear()