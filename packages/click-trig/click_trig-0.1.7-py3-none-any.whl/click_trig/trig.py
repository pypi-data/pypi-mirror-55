"""Trig click app

click app that returns the length of the hypotenuse by default and trig
funcs as options.
"""
import math

import click
from emoji import emojize


def pythagorean(a, b):
    """Home made Pythagorean func

    Function will use the Pythagorean forumla to return the length of
    hypotenuse.

    Formula
    -------
    a: int
        First Parameter is the length of the leg opposite or adjecents.

    b: int
        Second Paremeter is the length of leg adjecent or opposite.
    """
    return round(math.sqrt(a ** 2 + b ** 2), 4)


def sin_(num, opt="deg"):
    """Home made Sine Function

    Function will return Sine in degrees, by default, or radians
    when given the option of 'rad'.

    Formula
    -------
    Sine = Opposite / Hyptoneuse

    Parameters
    ----------
    num: int
        First parameter is the angle as an interger

    opt: str
        Second parameter excepts a string. "deg" for degrees
        is default. The string 'rad' will return Sine in
        radians.

    """
    if opt == "rad":
        return math.sin(num)
    else:
        return math.sin(math.radians(num))


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.version_option(message="trig v0.1.7 (c) 2019 Evan Baird")
@click.group(options_metavar="", context_settings=CONTEXT_SETTINGS)
def main():
    """Usage Examples:

    \b
    $ trig pythagoras <num1> <num2>


    Where <num1> and <num2> is the length of a or b for the variables
    in the Pythagorean formula.

    $ trig sine [OPTION -r|-radians] <num>

    Where <num> is the degree of the angle to return in degrees, by
    by default, or radians if -r|--radians is given for the option.
    """
    pass


@main.command(options_metavar="")
@click.argument("a", type=int)
@click.argument("b", type=int)
def pythagoras(a, b):
    """Returns the Length of Hypotneuse."""
    click.secho(
        emojize(
            f"The length of hypotenuse is :sparkles:{pythagorean(a, b)}:sparkles:."
        ),
        bold=True,
    )


@main.command(
    short_help="Return degrees(default) or radians with option.",
    options_metavar="[-r | --radians]",
)
@click.argument("sin", type=int)
@click.option(
    "-r", "--radians", "radians", is_flag=True, help="Returns angle in radians"
)
def sine(sin, radians):
    """Return angle in degrees by default
    add -r or --radians to get angle in radians."""
    if radians:
        click.secho(
            emojize(
                f"The Sine of Sin({sin}\xb0) in radians is :dizzy:{sin_(sin, 'rad'):.4f}:dizzy:."
            ),
            bold=True,
        )

    else:
        click.secho(
            emojize(
                f"The Sine of Sin({sin}\xb0) in degrees is :shortcake:{sin_(sin):.4f}:shortcake:."
            ),
            bold=True,
        )
