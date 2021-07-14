"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import time # for time.sleep()
from threading import Thread


class Consumer(Thread):
    """ Class that represents a consumer. """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """ Constructor.
        carts: List -- a list of add and remove operations
        marketplace: Marketplace -- a reference to the marketplace
        retry_wait_time: Time -- the number of seconds that a Consumer
                        must wait until the Marketplace becomes available
        kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time

    def run(self):
        """
        Every Consumer will ask for a cart from the Marketplace.
        Each cart will come with a set of add / remove operations.
        An operation consists of type, product and quantity:
        -- type: add or remove
        -- product: what kind product will be added / removed
        -- quantity: how many products will be added / removed
        An add operation can be succeeded or not:
        -- if succeeded, quantity will decrease
        -- if not succeeded (product is not in the marketplace),
            Consumer will wait (sleep) before retrying to add it.
        After all operations from a cart are completed, Consumer
        places their order (print a list of products from cart).
        """

        for cart in self.carts:
            cart_id = self.marketplace.new_cart()
            for operation in cart:
                quantity = operation["quantity"]
                while quantity:
                    if operation["type"] == "add" and self.marketplace.add_to_cart(
                            cart_id, operation["product"]) is False:
                        time.sleep(self.retry_wait_time)
                        continue
                    if operation["type"] == "remove":
                        self.marketplace.remove_from_cart(cart_id, operation["product"])
                    quantity -= 1
            self.marketplace.place_order(cart_id)
