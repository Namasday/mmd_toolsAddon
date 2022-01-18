# [blender]mmd_tools刚体类扩展插件（根据拓扑模型快速建立刚体脚本）

## 使用方法

1、手动建立需要物理的模型的低面数、四边面拓扑模型（最终刚体物理模拟的精度由此模型面数与骨骼数确定）

2、选中该拓扑模型，确保其是mmd_tools所建立的空物体子级

3、点击插件面板按钮，一键建立无父级刚体群

# 功能

1、物体模式下点击添加刚体，会对所有选择的网格物体的所有面建立刚体群（具有非三、四边面的物体可能会报错）

2、编辑模式下，先判断有没有选择面，无则按钮呈灰色，有则可以点击按钮，会根据选择的面一一创建刚体

## 思路建立

1、根据选择的物体，分别提取物体内各个面构成的4个点位置信息

2、以视口为基础，以视图向右为刚体x方向，视图向前为刚体y方向，视图向上为刚体z方向

3、计算世界坐标系下的几何中心，并定为创建刚体后的移动坐标

    (1) 比较出世界坐标系下各个轴向标量值较大两点的值并计算出其中间值，定义为大中间值

    (2) 比较出世界坐标系下各个轴向标量值较小两点的值并计算出其中间值

    (3) 计算两个中间值的中间值，设为该轴向上刚体需移动的距离

4、计算刚体的旋转值与尺寸信息（y方向设置为手动输入刚体厚度，默认为0.05）

    (1) 提取当前面的法向向量

    (2) 所需x、z尺寸 = （该尺寸轴向上的大中间值 - 该尺寸轴向上的中间值） / 法向向量该轴的值

    (3) 刚体的各轴旋转值 = 法向单位向量该轴的值 * 360

5、根据计算出的位置、旋转、尺寸数据，分别输入mmd_tool刚体面板建立刚体

## 预设面板

1、刚体x、z尺寸系数，可根据计算值拉长建立的刚体，以及刚体的y尺寸

2、建立完毕后是否删除原拓扑模型