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

### Installation using pip

You can install the tool using pip:

``` shell
pip install copycat
```

### Installation using AUR

If you are using an Arch-based distribution, you can install the tool using the AUR package:

``` shell
yay -S copycat
```

Remember to install the other dependencies from the AUR:

``` shell
yay -S python-pynput python-pyautogui python-ttkthemes
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

### How it works

First, you need to record a macro, you can do this by running the tool in GUI mode:

``` shell
copycat --gui
```

If you want to use a different theme, you can use the `--theme` option:

``` shell
copycat --gui --theme "arc"
```

Visit the [ttkthemes](https://ttkthemes.readthedocs.io/en/latest/themes.html) documentation to see all the available
themes.

#### Record a macro

Then you can record a macro by clicking the `record` button. Once you start recording, the GUI will hide so you can
perform any mouse and keyboard actions.
In every moment, press the `ESC` key to `pause` the recording.
You can resume the recording pressing again the `record` button, or you can complete the record process and save the
macro by clicking on the `save` button.
Select the name of the macro and click on the `save` button.

#### Replay a macro

Once you have a macro saved, you can replay it in two ways:

1. by clicking on the `replay` button, and selecting the macro you want to replay and the replay `speed` (1.0 is the
   real record speed).
2. by running the tool with the `--reply` option:

``` shell
copycat --reply <macro_name> --speed <speed>
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
[pydantic](https://docs.pydantic.dev/latest/), [pytest](https://docs.pytest.org/en/stable/), [ttkthemes](https://ttkthemes.readthedocs.io/en/latest/authors.html), [pynput](https://pynput.readthedocs.io/en/latest/) [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
and more, I simply put the pieces together. Please check and support all the tools and libraries used in this project.
