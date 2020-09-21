"""This module defines a simple Callback class."""

class Callback:
    """
    Callback class to execute functions at a later time.

    Attributes
    ----------
    func : function
        Function to be executed later
    args : tuple
        '*args' for func
    kwargs : dict
        '**kwargs' for func
    """

    def __init__(self, func, *args, **kwargs):
        """Initialize the class."""
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        """Execute the function"""
        return self.func(*self.args, **self.kwargs)