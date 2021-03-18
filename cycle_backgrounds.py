#!/usr/bin/python3 -u

'''
Created on 15/02/2013

Script to generate XML descriptor for background image cycle for MATE/GNOME2.

Based on tutorial: http://cobberlinux.wordpress.com/2012/10/06/tutorial-how-to-make-a-background-slideshow-mate/

You are free to use, modify and distribute this file as you want!

Basic usage:

1. Create a folder and copy the images to the folder.
2. Execute: python cycle_backgrounds.py --dir IMAGE_FOLDER
3. Select as desktop background the xml file generated on image folder (background.xml)

To advanced usage see help options executing:
python cycle_backgrounds.py -h

@author: Alexandre Fidelis Vieira Bitencourt
@author: Sergi Casbas. Python3 compatibility & randomize function.
'''

import os
import fnmatch

from optparse import OptionParser
from xml.dom.minidom import Document
from random import shuffle

def parse_args():
    parser = OptionParser()
    parser.add_option('-d', '--dir', dest='dir',
                      help='directory with background images to cycle', metavar='DIR')
    parser.add_option('-t', '--transition', dest='transition',
                      help='transition time in seconds (defaults to 5 seconds)',
                      metavar='TRANSITION_TIME', default='5')
    parser.add_option('-s', '--static', dest='static',
                      help='static time in seconds (defaults to 60 seconds)',
                      metavar='STATIC_TIME', default='60')
    parser.add_option('-o', '--output', dest='output',
                      help='background XML file name (defaults to background.xml)',
                      metavar="BACKGROUND_XML", default='background.xml')
    parser.add_option('-r', '--random', dest='randomize', action="store_true",
                      help='Automatically randomize file list (default false)',
                      metavar="", default=False)
    args = parser.parse_args()

    if args[0].dir is None:
        print ('Error: Image directory is required.\n')
        parser.print_help()
        return None

    if not os.path.isdir(args[0].dir):
        print ('Error: Invalid image directory.\n')
        parser.print_help()
        return None

    return args[0]

def generate_xml(args):
    images = []
    for f in os.listdir(args.dir):
        if fnmatch.fnmatch(f, "*.jpg") or \
            fnmatch.fnmatch(f, "*.gif") or \
            fnmatch.fnmatch(f, "*.png"):
            images.append(args.dir + os.path.sep + f)
    if len(images) == 0:
        print ('Error: Image directory contains no images.\n')
        return

    if args.randomize:
        shuffle(images)

    doc = Document()
    background = doc.createElement('background')
    doc.appendChild(background)

    # starttime
    starttime = doc.createElement('starttime')
    background.appendChild(starttime)
    year = doc.createElement('year')
    year.appendChild(doc.createTextNode('2000'))
    starttime.appendChild(year)
    month = doc.createElement('month')
    month.appendChild(doc.createTextNode('01'))
    starttime.appendChild(month)
    day = doc.createElement('day')
    day.appendChild(doc.createTextNode('01'))
    starttime.appendChild(day)
    hour = doc.createElement('hour')
    starttime.appendChild(hour)
    hour.appendChild(doc.createTextNode('00'))
    minute = doc.createElement('minute')
    minute.appendChild(doc.createTextNode('00'))
    starttime.appendChild(minute)
    second = doc.createElement('second')
    second.appendChild(doc.createTextNode('00'))
    starttime.appendChild(second)

    # process images
    imgs = iter(images)
    img = next(imgs)
    try:
        while True:
            static = doc.createElement('static')
            background.appendChild(static)
            duration = doc.createElement('duration')
            static.appendChild(duration)
            duration.appendChild(doc.createTextNode(args.static + ".0"))
            f = doc.createElement('file')
            static.appendChild(f)
            f.appendChild(doc.createTextNode(img))
            img2 = next(imgs)
            transition = doc.createElement('transition')
            background.appendChild(transition)
            duration = doc.createElement('duration')
            transition.appendChild(duration)
            duration.appendChild(doc.createTextNode(args.transition + ".0"))
            fro = doc.createElement('from')
            fro.appendChild(doc.createTextNode(img))
            transition.appendChild(fro)
# so that the image does not transition to itself
            img = img2
            to = doc.createElement('to')
            to.appendChild(doc.createTextNode(img))
            transition.appendChild(to)
    except StopIteration:
        pass

    f = open(args.dir + os.path.sep + args.output, 'w')
    f.write(doc.toprettyxml('    '))
    f.close()

if __name__ == '__main__':
    args = parse_args()
    if args is not None:
        generate_xml(args)
