# -*- coding:utf-8 -*-
"""
======================================
Radar chart (aka spider or star chart)
======================================

This example creates a radar chart, also known as a spider or star chart [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.

.. [1] http://en.wikipedia.org/wiki/Radar_chart
"""
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    # rotate theta such that the first axis is at the top
    theta += np.pi/2

    def draw_poly_patch(self):
        verts = unit_poly_verts(theta)
        return plt.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts


def example_data():
    data1 = [
        ['ZL','ZR','ZF','ZM','ZC'],
        ('RadarPicture',[
          [0.063,-0.0040000000000000001, -0.22600000000000001,-0.22900000000000001,2.1949999999999998],
          [1.161, -0.377, -0.086999999999999994, -0.095000000000000001, -0.159],
          [0.48299999999999998,-0.79900000000000004,2.4830000000000001,2.4249999999999998,0.308],
          [-0.314,1.6859999999999999,-0.57399999999999995,-0.53700000000000003,-0.17299999999999999],
          [-0.69999999999999996, -0.41499999999999998, -0.161, -0.161, -0.253]])
    ]
    return data1

# if __name__ == '__main__':
#     N = 5
#     plt.rc('figure', figsize=(9, 9))
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     plt.rcParams['axes.unicode_minus'] = False
#     theta = radar_factory(N, frame='polygon')
#     data = example_data()
#     spoke_labels = data.pop(0)
#
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='radar')  # 创建axes类
#     fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05) # 可以轻而易举地修改间距，此外，它也是个顶级函数
#     colors = ['b', 'r', 'g', 'm', 'y']
#     title = data[0][0]
#     ax.set_title(title, weight='bold', size='medium', position=(0.5, 1.06),horizontalalignment='center', verticalalignment='center')
#     ax.set_varlabels(spoke_labels)
#     data = data[0][1]
#     ax.set_rgrids([0.5, 1, 1.5, 2, 2.5]) # set_rgrids方法用于设置极径网格线显示 （！！！这句话必须有，否则出错！）
#     for d, color in zip(data, colors):
#         ax.plot(theta, d,'-o', lw=2, color = color)
#         ax.fill(theta, d,facecolor = color, alpha = 0.25)
#     labels = (list('abcde'))
#     legend = ax.legend(labels, loc='best',labelspacing=0.1, fontsize='small')
#     fig.text(0.5, 0.965, u'这是参考官网上的雷达图的画法画的单个图',  #text()自由添加文本的最大作用就是注释
#              horizontalalignment='center', color='black', weight='bold',
#              size='large')
#     plt.savefig('singleRaderPic.jpg')
#     plt.show()

# '''定义画一个雷达图的函数
# itemnames表示各个指标的名字，类型是列表
# data表示各个用户对应指标的数值，类型是二维列表或二维数组
# title输出图片的标题，类型是字符串
# rgrids设置极径网格线显示，列表类型,默认为[0.5,1,1.5,2]，必须是正数
# labels表示各个用户的名称，类型是列表
# saveas 表示将文件存储的名称，类型是字符串
# '''
def drawRader(itemnames,data,title,labels,saveas,rgrids =[0.5,1,1.5,2] ):
    N = len(itemnames)
    fig = plt.figure()
    plt.rc('figure',figsize=(9, 9))

    plt.rcParams['font.size'] = 14
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    theta = radar_factory(N, frame='polygon')

    ax = fig.add_subplot(111, projection='radar')  # 创建axes类
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05) # 可以轻而易举地修改间距，此外，它也是个顶级函数
    colors = list('bgrcmyckw'[:len(data)])  # 此处颜色最多九个
    ax.set_title(title, weight='bold', size=18, position=(0.5, 1.06),horizontalalignment='center', verticalalignment='center')
    ax.set_varlabels(itemnames)
    ax.set_rgrids(rgrids) # set_rgrids方法用于设置极径网格线显示 （！！！这句话必须有，否则出错！）
    for d, color in zip(data, colors):
        ax.plot(theta, d,'-o', lw=2, color = color)
        ax.fill(theta, d,facecolor = color, alpha = 0.25)
    labels = (labels)
    legend = ax.legend(labels, loc='best',labelspacing=0.1, fontsize='small')
    fig.text(0.5, 0.965, u'这是参考官网上的雷达图的画法画的单个图',  #text()自由添加文本的最大作用就是注释
             horizontalalignment='center', color='black', weight='bold',
             size='large')
    plt.savefig(saveas)
    plt.show()


data = np.array([[-0.70015891, -0.41487809, -0.16097726, -0.16079873, -0.25300721],
       [ 1.1608426 , -0.37750679, -0.08656954, -0.09435831, -0.15737999],
       [ 0.06020027, -0.00516616, -0.22514674, -0.22836873,  2.19668056],
       [-0.31369849,  1.68538296, -0.57390549, -0.53679005, -0.17339869],
       [ 0.48361139, -0.79980286,  2.48638397,  2.42649433,  0.30897407],
       ])

title = 'RadarPicture'
rgrids = [0.5, 1, 1.5, 2, 2.5]

itemnames = ['ZL','ZR','ZF','ZM','ZC']
labels = list('abcde')
drawRader(itemnames=itemnames,data=data,title=title,labels=labels, saveas = '1.jpg',rgrids=rgrids)
