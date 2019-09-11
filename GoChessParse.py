import os
import cv2
import click
import unittest
from app import create_app
from app.cv_parse import ssd_net
from app.cv_parse.ChessBoardParser import ChessBoardParser


@click.group()
def cli():
    pass


@click.command()
def test():
    '''
    start unit test
    '''
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@click.command()
def run():
    '''
    run flask web server
    '''
    app = create_app()
    app.run(host='127.0.0.1', port=2048)


@click.command()
@click.argument('image_path')
def input_image(image_path):
    '''
    output result with web server
    '''

    parser = ChessBoardParser()
    image = cv2.imread(image_path)
    center_lists = ssd_net.detect_chesspieces(InputArray=image)
    ChessBoardParser.draw_chesspieces_locate(image=image, center_lists=center_lists)
    output_matrix = parser.output(image,center_lists)
    print(output_matrix)


cli.add_command(test)
cli.add_command(run)
cli.add_command(input_image)

if __name__ == '__main__':
    cli()
