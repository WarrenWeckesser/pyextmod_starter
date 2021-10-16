

from pyextmod_starter import generate_extmod


def process(x, /, y, *, z, alpha=None, beta=1):
    """
    process(x, /, y, *, z, alpha, beta)

    This is the docstring for process().
    """
    pass


def tabulate(x):
    """Docstring for tabulate."""
    pass


example_mod_docstring = """
Docstring for the example module.

The module defines the functions process() and tabulate().
"""

# Use the default filenames for output.
generate_extmod("example", example_mod_docstring, [process, tabulate])
