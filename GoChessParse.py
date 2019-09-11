import os
import click
import unittest
from app import create_app
from app.cv_parse import output_result


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
    app.run(host='0.0.0.0',debug=False)


@click.command()
@click.argument('image_path')
def input_image(image_path):
    '''
    output result with web server
    '''
    print(output_result(image_path, False))


cli.add_command(test)
cli.add_command(run)
cli.add_command(input_image)

if __name__ == '__main__':
    cli()
