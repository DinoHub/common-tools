from basic_image_eda import BasicImageEDA
from logzero import logger
import click


@click.group()
def intro():
    pass


@click.command()
@click.option('--imagepath', required=True, help='Absolute path to folder of raw images')
@click.option('--extensions', default="jpg,jpeg,png", help='List of file extensions to read. Default: jpg,jpeg,png')
def dimensions(imagepath=None, extensions=None):
    extensionsList=extensions.split(',')
    BasicImageEDA.explore(data_dir=imagepath, extensions=extensionsList, threads=0, dimension_plot=True, hw_division_factor=1.0)    

intro.add_command(dimensions)    

if __name__=='__main__':
    intro()