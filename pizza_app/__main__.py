"""Package entrypoint.

Run with (from \pizza-app\pizza-app):
    py -m pizza_app
"""

from .application import PizzaApplication

if __name__ == "__main__":
    PizzaApplication().run()
