import spiceypy as sp

# 加载内核
sp.furnsh('kernels/lsk/naif0012.tls')
sp.furnsh('kernels/spk/de430.bsp')
sp.furnsh('kernels/pck/pck00011.tpc')

et0 = sp.str2et("2007 JAN 01 00:00:00 TDB")
et1 = sp.str2et("2007 APR 01 00:00:00 TDB")
cnfine = sp.cell_double(2)
sp.wninsd(et0, et1, cnfine)
result = sp.cell_double(1000)

# 计算月球与地球之间的距离大于 400000 km 的时间间隔
sp.gfdist(
    "moon", "none", "earth", ">", 400000, 0.0, sp.spd(), 1000, cnfine, result
)

count = sp.wncard(result)
results = []
# 遍历结果，将每个时间间隔的左右端点转换为字符串并添加到 results 列表中
for i in range(0, count):
    left, right = sp.wnfetd(result, i)
    timstr_left = sp.timout(
        left, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
    )
    timstr_right = sp.timout(
        right, "YYYY-MON-DD HR:MN:SC.###### (TDB) ::TDB ::RND", 41
    )
    results.append(timstr_left)
    results.append(timstr_right)

# 打印结果
print(*results, sep='\n')

sp.kclear()