import matplotlib.pyplot as plt
import numpy as np


class Plotter:								
        _x = 1
        _y = 1
        _xname='x-axis'
        _yname='y-axis'
        _title='title'

        def __init__(self,x,y,title,xlabel,ylabel):
                self._x = x
                self._y = y
                self._title = title
                self._xname = xlabel
                self._yname = ylabel
                plt.title(self._title)
                plt.xlabel(self._xname)
                plt.ylabel(self._yname)
                plt.plot(self._x,self._y, color="red")
                plt.show()
        

        
#test
x=[1,2,3,4,5,6,7,8,9,10,11,12]
y=[6351,7132,9081,11099,12079,14466,13027,14939,17423,16590,16672,12627]
p1 = Plotter(x,y,'title','month','number of passengers')
p1.showplot