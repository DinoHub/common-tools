from logzero import logger
import click
import glob
import os
import cv2
import imutils
from PIL import Image, ImageOps

# -*- coding: utf-8 -*-
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

@click.group()
def intro():
    pass


@click.command()
@click.option('--srcimagepath', required=True, help='Absolute path to source folder of raw images')
@click.option('--dstimagepath', required=True, help='Absolute path to destination folder of resized images')
@click.option('--width', required=True, help='Resize to width in pixels')
@click.option('--extensions', default="jpg,jpeg,png", help='List of file extensions to read. Default: jpg,jpeg,png')
def resizewithaspectratio(srcimagepath=None, extensions=None, width=None, height=None, dstimagepath=None):
    logger.debug("srcimagepath: " +srcimagepath )
    srcpath=srcimagepath+"/**"
    logger.debug("srcpath: " +srcpath)
    srcImagefiles=[]
    for filetype in extensions.split(","):
        srcImagefiles=srcImagefiles+glob.glob(srcpath+'/*.'+filetype)
    
    for filename in srcImagefiles:
        logger.debug("Reading filename:" + filename)
        im=cv2.imread((filename))
        imresized=imutils.resize(im, width=int(width))
        logger.debug("Writing to "+dstimagepath+"/"+filename.split("/")[-1])
        cv2.imwrite(dstimagepath+"/"+str(filename).split("/")[-1], imresized)

@click.command()
@click.option('--srcimagepath', required=True, help='Absolute path to source folder of raw images')
@click.option('--dstimagepath', required=True, help='Absolute path to destination folder of resized images')
@click.option('--width', required=True, help='Resize to width in pixels', type=int)
@click.option('--height', required=True, help='Resize to height in pixels', type=int)
@click.option('--extensions', default="jpg,jpeg,png", help='List of file extensions to read. Default: jpg,jpeg,png')
def resizeAspectratioBorder(srcimagepath=None, extensions=None, width=None, height=None, dstimagepath=None):
    logger.debug("srcimagepath: " +srcimagepath )
    srcpath=srcimagepath+"/**"
    logger.debug("srcpath: " +srcpath)
    srcImagefiles=[]
    for filetype in extensions.split(","):
        srcImagefiles=srcImagefiles+glob.glob(srcpath+'/*.'+filetype)
    
    for filename in srcImagefiles:
        logger.debug("Reading filename:" + filename)        
        im = Image.open(filename)
        im = ImageOps.pad(im, (width, height), color='grey')
        logger.debug("Writing to "+dstimagepath+"/"+filename.split("/")[-1])
        im.save(dstimagepath+"/"+str(filename).split("/")[-1])        


@click.command()
@click.option('--srcimagepath', required=True, help='Absolute path to source folder of raw images')
@click.option('--dstimagepath', required=True, help='Absolute path to destination folder of resized images')
@click.option('--extensions', show_default=True, default="jpg,jpeg,png", help="List of file extensions to read. Default: jpg,jpeg,png")
@click.option('--texttype', show_default=True, required=True, default="fixedText", type=click.Choice(['fixedText', 'runningNumber'], case_sensitive=False), help="fixedText: A fixed text for all images, runningNumber: a running number for each image")
@click.option('--text', required=False, help='Fixed text to overlay')
def addTextOverlay(srcimagepath=None, dstimagepath=None, extensions=None, texttype=None, text=None):    
    
    if (texttype=="runningNumber"):
        counter=0
    else:
        text=text

    logger.debug("srcimagepath: " +srcimagepath )
    srcpath=srcimagepath
    logger.debug("srcpath: " +srcpath)
    srcImagefiles=[]
    for filetype in extensions.split(","):
        logger.debug("Preparing for " + srcpath+'/*.'+filetype)
        logger.debug("Preparing for " + srcpath+'/**/*.'+filetype)
        srcImagefiles=srcImagefiles+glob.glob(srcpath+'/**/*.'+filetype)
        srcImagefiles=srcImagefiles+glob.glob(srcpath+'/*.'+filetype)
    
    logger.debug("Total files: " + str(len(srcImagefiles)))
    for filename in srcImagefiles:
        logger.debug("Reading filename:" + filename)
        im=cv2.imread((filename))

        if (texttype=="runningNumber"):            
            text=str(counter)
            counter=counter+1
        logger.debug("Writing text as:" + text)
        width=im.shape[0]
        height=im.shape[1]
        logger.debug("Image size is " + str(width) + ":" + str(height))
        im = cv2.putText(im, text, (10,width-10), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 3, cv2.LINE_AA)
        logger.debug("Writing to "+dstimagepath+"/"+text.zfill(5)+"."+filename.split(".")[-1])
        cv2.imwrite(dstimagepath+"/"+text.zfill(5)+"."+filename.split(".")[-1], im)
        # break;

intro.add_command(resizewithaspectratio)    
intro.add_command(addTextOverlay)   
intro.add_command(resizeAspectratioBorder)

if __name__=='__main__':
    intro()