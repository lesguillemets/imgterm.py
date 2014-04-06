#!/usr/bin/env python3
# coding:utf-8

from textwrap import dedent
import PIL.Image as img
import numpy as np
import sys
from rgbtoansi import colorize_bg
from rgbtoansi import grayscale_bg
from rgbtoansi import *
from kluster import Kluster

def get_termsize():
    try:
        import fcntl, termios, struct
        h, w, _, _ = struct.unpack(
            'HHHH',
            fcntl.ioctl(
                sys.stdout.fileno(),
                termios.TIOCGWINSZ,
                struct.pack('HHHH', 0, 0, 0, 0)))
    except OSError:
        import os
        h, w = map(int,os.popen('stty size', 'r').read().split())
    return w, h

def show_img(imgfile, widthratio=2/3, fontratio=2.5, method="upperleft"):
    '''
    imgfile : image file readable by PIL.Image.open
    widthratio : how much of terminal width the image uses
    fontratio : the ratio height/width of your font
    about 2 for monaco, 2.5 for ubuntu mono.
    returns list of lines.
    '''
    w, _ = get_termsize()
    w = int(w*widthratio)
    imgary = np.array(img.open(imgfile))
    imgheight, imgwidth = len(imgary), len(imgary[0])
    mode = ''
    if len(imgary.shape) == 2:
        mode = 'grayscale'
    elif len(imgary.shape) == 3:
        if imgary.shape[2] == 3:
            mode = 'rgb'
        elif imgary.shape[2] == 4:
            mode = 'rgba'
    if mode == '':
        raise IOError("Unknown filetype?")
    marks = [int(i*imgwidth/w) for i in range(w+1)]
    rowpixels = (imgwidth/w)*fontratio  # 2 for monaco, 2.5 for ubuntu mono
    if method == 'ascii':
        dimmer = Kluster(2, threshold=marks[0]*rowpixels/100)
    yreadingstart = 0
    img_str = []
    while yreadingstart < imgheight-1:
        line = []
        for (i,m) in enumerate(marks[1:]):
            m_b = marks[i]
            if method == "ascii":
                grid = imgary[yreadingstart:yreadingstart+rowpixels,
                                  m_b:m]
                if mode == 'rgb':
                    grid = grid.reshape(-1,3)
                elif mode == 'rgba':
                    grid = grid.reshape(-1,4)
                elif mode == 'grayscale':
                    grid = grid.flatten()
                dimmer.feeddata(grid)
                clusters = dimmer.analyse()
                # FIXME : some hard codings here.
                cls0 = clusters.count(0)
                cls1 = clusters.count(1)
                clsratio = cls0/(cls0+cls1)
                pixel0, pixel1 = dimmer.means
                if cls0 > cls1:
                    bgcolor, fgcolor = pixel0, pixel1
                else:
                    bgcolor, fgcolor = pixel1, pixel0
                bgcolor = list(map(int, bgcolor))
                fgcolor = list(map(int, fgcolor))
                if (0.2 < clsratio< 0.8 and
                    # if there are enough pixels for each to consider
                    dimmer._dist(pixel0, pixel1) > 100):
                        # and if there's been significant difference
                        
                        if abs(clsratio - 0.5) <0.15:
                            char = 'W'
                        else:
                            char = '+'
                        
                        if mode == 'rgb':
                            line.append(
                                set_color(fgcolor,bgcolor)+
                                char+ clear_style()
                            )
                        elif mode == 'rgba':
                            line.append('{}{}{}'.format(
                                set_color(fgcolor[:3], bgcolor[:3]),
                                char, clear_style()
                            ))
                        elif mode == 'grayscale':
                            line.append(grayscale_fg(fgcolor,
                                         grayscale_bg(bgcolor, char)))
                else :
                    if mode == 'rgb':
                        line.append(colorize_bg(' ', list(bgcolor)))
                    elif mode == 'rgba':
                        line.append(colorize_bg(' ', list(bgcolor)[:3]))
                    elif mode == 'grayscale':
                        line.append(grayscale_bg(' ', bgcolor))
            else:
                if method == "upperleft":
                    pixel = imgary[yreadingstart,m_b]
                elif method == "mean":
                    grid = imgary[yreadingstart:yreadingstart+rowpixels,
                                  m_b:m]
                    if mode == 'grayscale':
                        pixel = sum(grid.flatten())/float(
                            grid.shape[0]*grid.shape[1])
                    else:
                        if mode == 'rgb':
                            pixel = np.array((0,0,0))
                        elif mode == 'rgba':
                            pixel = np.array((0,0,0,0))
                        for y_ in range(len(grid)):
                            for x_ in range(len(grid[0])):
                                pixel += grid[y_,x_]
                        pixel = pixel//(len(grid)*len(grid[0]))
                
                if mode == 'rgb':
                    line.append(colorize_bg(' ', list(pixel)))
                elif mode == 'rgba':
                    line.append(colorize_bg(' ', list(pixel)[:3]))
                elif mode == 'grayscale':
                    line.append(grayscale_bg(' ', pixel))
        yreadingstart += rowpixels
        img_str.append(''.join(line))
    return img_str


def test():
    testfile = 'kitten.jpg'
    show_img(testfile,1/2,2)
    print("______________________________")
    show_img(testfile,1/2,2, 'mean')


def main():
    filenames = sys.argv[1:]
    if not filenames:
        print("specify filename(s).")
        return
    
    for filename in filenames:
        try:
            imgstr = show_img(filename ,method='ascii')
            for line in imgstr:
                print(line)
            print("+++++++++++++++++++++++++++++++++++")
            imgstr = show_img(filename, method='mean' )
            for line in imgstr:
                print(line)
        except IOError:
            print("No file found. Or something like that.")
            continue


if __name__ == "__main__":
    main()
