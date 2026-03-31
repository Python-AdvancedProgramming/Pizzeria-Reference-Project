"""Package entrypoint.

Run with (from project root):
    py -m pizza_app
"""

from .application import PizzaApplication

if __name__ == "__main__":
    PizzaApplication().run()
