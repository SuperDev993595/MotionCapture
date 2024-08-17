# Copycat

`copycat` is a tool that record and replay mouse and keyboard macro.

## Demo

This is a short demo of the tool:

https://github.com/user-attachments/assets/4ce6616e-8fa1-4efb-8c31-f31bfe8e827c

## Installation

This tool uses [poetry](https://python-poetry.org/) to manage dependencies and packaging. To install all the
dependencies simply run:

``` shell
poetry install
```

## Usage

You can run the tool using poetry:

``` shell
poetry run copycat --help
```

Or you can run the tool using python:

``` shell
python -m copycat --help
```

Or you can run the tool directly from the directory or add it to your path:

``` shell
copycat --help
```

```shell
usage: copycat [-h] [--verbose] [--debug] [--quiet | --no-quiet | -q] [--version] [--gui] [--theme THEME] [--speed SPEED] [--reply REPLY]

Copycat is a tool that record and replay mouse and keyboard macro.

options:
  -h, --help            show this help message and exit
  --verbose, -v         Increase verbosity. Use more than once to increase verbosity level (e.g. -vvv).
  --debug               Enable debug mode.
  --quiet, --no-quiet, -q
                        Do not print any output/log
  --version, -V         Show version and exit.
  --gui                 Run the tool in GUI mode.
  --theme THEME, -t THEME
                        Set the "ttkthemes" GUI theme. (Default: equilux)
  --speed SPEED, -s SPEED
                        Speed of the macro playback. (Default: 1.0)
  --reply REPLY, -r REPLY
                        Define macro name to reply.
```

## Development

### Testing

To run the tests simply run:

``` shell
poetry run test
```

### Update `setup.py`

To update the `setup.py` file with the latest dependencies and versions run:

``` shell
poetry run poetry2setup > setup.py
```

### Acknowledgements

This project was generated using powerful tools and libraries such as [poetry](https://python-poetry.org/),
[pydantic](https://docs.pydantic.dev/latest/), [pytest](https://docs.pytest.org/en/stable/) and more, I simply put the
pieces together. Please check and support all the tools and libraries used in this project.
