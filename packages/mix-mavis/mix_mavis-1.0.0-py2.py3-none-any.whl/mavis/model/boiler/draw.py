# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2014-2019 Mixlinker Networks Inc. <mixiot@mixlinker.com>
# All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Application License of Mixlinker Networks License and Mixlinker
# Distribution License which accompany this distribution.
#
# The Mixlinker License is available at
#    http://www.mixlinker.com/legal/license.html
# and the Mixlinker Distribution License is available at
#    http://www.mixlinker.com/legal/distribution.html
#
# Contributors:
#    Mixlinker Technical Team
###############################################################################
# Description : 自定义动态画图模块
# Author : zhaoguangjun

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class Draw():
    def __init__(self, x, y):
        """

        :param data:
        """
        self.x = x
        self.y = y
        self.fig, self.ax = plt.subplots()
        self.xdata, self.ydata = [], []
        self.ln = self.ax.plot([], [], 'r-', animated=False)

        super(Draw, self).__init__()

    # def init_func(self):
    #     self.ax.set_xlim(0, 2 * np.pi)
    #     self.ax.set_ylim(-1, 1)
    #     return self.ln

    def __call__(self):
        return self.plot_((self.x, self.y))

    def update(self, data):
        print("data is:", data[0], data[1])
        self.xdata.append(data[0])
        self.ydata.append(data[1])
        self.ln.set_data(self.xdata, self.ydata)
        return self.ln

    def plot_(self, n):
        # 这里的frames在调用update函数时会将frames作为实参传递给“data”
        ani = FuncAnimation(fig=self.fig, func=self.update, frames=n)
        plt.show()
