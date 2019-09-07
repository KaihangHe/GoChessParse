import os
import click
import unittest
from app import create_app
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
    print("flasky")
    app = create_app()
    app.run()


@click.command()
@click.argument('image_path')
def input_image(image_path):
    '''
    output result with web server
    '''
    import cv2
    image = cv2.imread(image_path)
    parser = ChessBoardParser()
    output_matrix = parser.output(image)
    print(output_matrix)


cli.add_command(test)
cli.add_command(run)
cli.add_command(input_image)

if __name__ == '__main__':
    cli()
