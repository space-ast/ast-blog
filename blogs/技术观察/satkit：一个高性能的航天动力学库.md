# satkit: 一个高性能的航天动力学库

[satkit（Satellite Toolkit）](https://github.com/ssmichael1/satkit)是一个高性能的航天动力学库，具有轨道预报、坐标转换、时间系统转换等航天动力学基础功能。

> 本文主要介绍其功能模块、使用方法和部分技术细节。具体实现请参考[satkit 代码仓库](https://github.com/ssmichael1/satkit)。


## 功能模块

### 坐标系转换

satkit 可以实现多种坐标系之间的转换，包括：

- **ITRF** - 国际地球坐标系（地球固连系）
- **GCRF** - 地心天球坐标系（地球惯性系），采用 IAU-2000/2006 规范
- **CIRF** - 天球中间坐标系
- **TIRF** - 地球中间坐标系
- **TEME** - 真春分点平赤道系

### 轨道预报

提供了多种轨道预报方法：

- **高精度轨道预报**：
  - 使用自适应步长的 Runge-Kutta 9(8) 方法积分
  - 支持灵活配置的力模型：地球引力场、三体引力、大气阻力、太阳辐射光压
  - 支持积分STM状态转移矩阵，用于协方差预报

- **二体轨道预报**：解析的开普勒预报

- **SGP4轨道预报**：两行轨道根数（TLE）预报器

### 时间系统

可以实现不同时间尺度之间的转换：

- **UTC** - 协调世界时，带闰秒处理
- **TAI** - 国际原子时
- **TT** - 地球时
- **TDB** - 质心动力学时
- **UT1** - 带地球定向修正的世界时
- **GPS** - GPS 时间

## 使用示例

下文展示了satkit所提供的python接口的使用方法，详细的使用方法和更复杂的示例可以参考[satkit的Python库文档](https://satellite-toolkit.readthedocs.io/latest/)


### 安装

可以通过以下命令安装satkit的Python库。

```bash
pip install satkit
```



### 坐标转换示例

```python
import satkit as sk

# 创建时间点
time = sk.time(2024, 1, 1, 12, 0, 0)

# 定义 ITRF（地固系）坐标系中的位置
itrf_pos = sk.itrfcoord(latitude_deg=42.0, longitude_deg=-71.0, altitude=100.0)

# 获取 ITRF 到 GCRF（惯性）的旋转四元数
q = sk.frametransform.qitrf2gcrf(time)

# 转换到 GCRF
gcrf_pos = q * itrf_pos.vector
print(f"GCRF 位置: {gcrf_pos}")
```

### 高精度轨道预报示例

```python
import satkit as sk
import numpy as np

# 初始状态向量 [x, y, z, vx, vy, vz] (GCRF 坐标系)
r0 = 6378e3 + 500e3  # 500 km 高度
v0 = np.sqrt(sk.consts.mu_earth / r0)
state0 = np.array([r0, 0, 0, 0, v0, 0])

# 开始时间
time0 = sk.time(2024, 1, 1)

# 力模型配置
settings = sk.propsettings()
settings.gravity_order = 8
settings.use_spaceweather = True

# 预报 1 天
result = sk.propagate(
    state0,
    time0,
    end=time0 + sk.duration.from_days(1),
    propsettings=settings
)

# 插值查询任何时间的状态
query_time = time0 + sk.duration.from_hours(6)
state = result.interp(query_time)
print(f"6 小时后的状态: {state}")
```

### SGP4 预报示例

```python
import satkit as sk

# 加载 TLE
lines = [
    "ISS (ZARYA)",
    "1 25544U 98067A   24001.50000000  .00016717  00000-0  10270-3 0  9003",
    "2 25544  51.6432 351.4697 0007417 130.5364 329.6482 15.48915330299357"
]
tle = sk.TLE.from_lines(lines)

# TLE 预报
time = sk.time(2024, 1, 2)
pos, vel = sk.sgp4(tle, time)
print(f"ISS 位置: {pos}")
```



## 技术细节

### 性能与接口优化

- **SIMD 友好**：使用CPU的SIMD指令加速矢量运算

- **内存高效**：多使用静态的栈内存，减少动态内存分配

- **并行处理**：提供了线程安全的 API，支持多颗卫星的并发预报

- **Python接口**：通过[PyO3](https://github.com/PyO3/pyo3) 实现了高效的 Python 接口封装

### 数据依赖


1. 核心数据文件

核心数据只需要单次下载，一般不需要更新：

- **[JPL 星历](https://ssd.jpl.nasa.gov/ephem.html)**：DE440/DE441 行星星历

- **[引力场模型](https://icgem.gfz.de/home)**：JGM2、JGM3、EGM96等球谐系数

- **[IERS 章动表](https://www.iers.org/IERS/EN/Publications/TechnicalNotes/tn36.html)**：IAU-2006 章动系列系数

2. 动态数据文件

动态数据需要定时更新：

- **[空间天气数据](https://celestrak.org/SpaceData/)**：F10.7 太阳通量、Ap 地磁指数

- **[地球指向参数](https://celestrak.org/SpaceData/)**：极移 (x, y)、UT1-UTC 时差、日长变化


### 内存安全性

satkit的底层采用[Rust语言](https://rust-lang.org/)实现，通过Rust严格的所有权和生命周期管理机制，确保内存安全与并发安全，同时保证了代码的执行效率

### 验证和测试

satkit库包含较为全面的测试，确保计算的正确性：

- **JPL 星历**
  - 根据 JPL 提供的切比雪夫多项式插值测试对比文件进行验证
  - 超过 10,000 个测试用例，覆盖所有行星和时间范围
  - 精度验证在 JPL 公布的公差范围内（亚米精度）

- **SGP4**：
  - 使用原始 C++ 分发版中的官方测试对比文件进行验证
  - 包含 Vallado 的 SGP4 实现的所有测试用例
  - 包括了边界情况和错误条件的测试

- **坐标转换**：
  - 通过多个参考实现进行交叉验证
  - 与SOFA 库比较，验证IAU-2006 规范下的转换精度
  - 与Vallado 的 GCRF ↔ ITRF 转换用例对比

- **高精度轨道预报**：
  - 与商业软件的相关功能模块进行对比验证
  - 多天预报的精度达到亚米级


## 总结

本文参考了satkit的官方文档、README文件以及其代码仓库，主要介绍了satkit的功能模块、使用方法和部分技术细节。

satkit 是一个底层由Rust语言实现的航天动力学库，其将Rust语言的高性能和安全性与Python的易用性相结合，能够为高精度轨道预报、航天任务规划、空间态势感知等计算场景提供一个**可选的解决方案和工具**，或许能够加入您的工具箱。