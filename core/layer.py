import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
import frameworks.keras.layers
import sys
import core.colors

layer_width = 40
layer_margin = 10

positions = 0

layers = []

class layer():
    def __init__(self,visible_top, visible_bottom,visible_left,visible_right,size_x,size_y):
        self.visible_top = visible_top
        self.visible_bottom = visible_bottom
        self.visible_left = visible_left
        self.visible_right = visible_right
        self.actual_left = float('inf')
        self.actual_top = float('-inf')
        self.actual_bottom = float('-inf')
        self.size_x = size_x
        self.size_y = size_y
        self.mappingText = ""
        self.titleText = ""
        self.mappingMiddleY = 0


#def get_effective_area():
#    return layer_width - layer_margin

def add_layer(patches, colors, size=24, num=5,
              position = 0, titleText = None, mappingText = None
              ):
    if num > 6:
        num = 6
    size = (size/frameworks.keras.layers.max_kernel_size_x)*layer_width
    ne_loc = [size/15,-1*size/15]


    #top_left = [position*layer_width, position]
    pos_left = 0
    if len(layers) > 0:
        pos_left = layers[-1].visible_right+10
    top_left = [pos_left, position]

    top_left = np.array(top_left)
    ne_loc = np.array(ne_loc)
    tp = np.array([0, size])
    loc_start = top_left - tp

    print([loc_start, num, ne_loc])

    post = loc_start + num * ne_loc

    left = post[0]

    bottom = post[1]
    print (["bottom", bottom])
    top = bottom+size
    right = left + size
    objlay = layer(top, bottom, left, right,size,size)

    for ind in range(num):
        pos = loc_start + ind * ne_loc
        patches.append(Rectangle(pos, size, size))
        if ind % 2:
            colors.append(core.colors.Medium)
        else:
            colors.append(core.colors.Light)
        if pos[0] < objlay.actual_left:
            objlay.actual_left = pos[0]
        if pos[1] > objlay.actual_bottom:
            objlay.actual_bottom = pos[1]

    objlay.actual_top = objlay.actual_bottom+size
    objlay.mappingText = mappingText
    objlay.titleText = titleText

    layers.append(objlay)

def add_mapping(patches, colors, index, ax, start_ratio = [0.2,0.2], patch_size=0.2):

    start_loc = [layers[index].visible_left+ (layers[index].size_x*start_ratio[0]),layers[index].visible_bottom + (layers[index].size_y*start_ratio[1])]

    end_loc = [layers[index+1].visible_left+ (layers[index+1].size_x*start_ratio[0]),layers[index+1].visible_bottom + (layers[index+1].size_y*start_ratio[1])]


    patch_size = patch_size*layers[index].size_x
    patches.append(Rectangle(start_loc, patch_size, patch_size))
    colors.append(core.colors.Dark)

    ratio = layers[index+1].size_y*0.7

    #layers[index].mappingMiddleY =

    ax.add_line(Line2D([start_loc[0], end_loc[0]],
                          [start_loc[1], end_loc[1]+ratio]))
    ax.add_line(Line2D([start_loc[0] + patch_size, end_loc[0]],
                          [start_loc[1], end_loc[1]+ratio]))
    ax.add_line(Line2D([start_loc[0], end_loc[0]],
                          [start_loc[1] + patch_size, end_loc[1]+ratio]))
    ax.add_line(Line2D([start_loc[0] + patch_size, end_loc[0]],
                          [start_loc[1] + patch_size, end_loc[1]+ratio]))

def label(index, plt, ax, text = None, top= False, xy_off=[0, 4]):
    xy_off=[0, 4]

    visible_y = 0
    if top == False:
        pos_y = min(layers[index].visible_bottom, layers[index+1].visible_bottom)- xy_off[1] #layers[index].visible_bottom + xy_off[0]+ ((layers[index+1].visible_bottom - layers[index].visible_bottom) //2)
        pos_x = layers[index].visible_left + xy_off[0]+ ((layers[index+1].visible_left - layers[index].visible_left) //2)
        if text == None:
            text = layers[index].mappingText
        plt.text(pos_x, pos_y, text, family='sans-serif', size=8,horizontalalignment='left',
         verticalalignment='top')
    else:
        pos_y = layers[index].actual_top + xy_off[1]
        pos_x = layers[index].actual_left + xy_off[0]
        if text == None:

            text = layers[index].titleText

        plt.text(pos_x, pos_y, text, family='sans-serif', size=8,horizontalalignment='left',
         verticalalignment='bottom')
