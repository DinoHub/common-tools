from logzero import logger
import click
import glob
import os
import cv2
import imutils


@click.group()
def intro():
    pass


@click.command()
@click.option('--srcimagepath', required=True, help='Absolute path to source folder of raw images')
@click.option('--dstimagepath', required=True, help='Absolute path to destination folder of resized images')
@click.option('--width', required=True, help='Resize to width in pixels')
@click.option('--height', required=True, help='Resize to height in pixels')
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
    
intro.add_command(resizewithaspectratio)    

if __name__=='__main__':
    intro()