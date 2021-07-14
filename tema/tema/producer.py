"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time # for time.sleep()
from threading import Thread


class Producer(Thread):
    """ Class that represents a producer. """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """ Constructor.
        products: List() -- a list of products that the producer will produce
        marketplace: Marketplace -- a reference to the marketplace
        republish_wait_time: Time -- the number of seconds that a Producer
                            must wait until the Marketplace becomes available
        kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        """
        Publish every product in the list of products, based on:
        -- product[0]: the id of the product that will be published
        -- product[1]: how many products from that product to publish
        -- product[2]: number of seconds for Producer to wait before
                        another publish call if the method succeeded
        ! publish method will fail if the buffer in Marketplace is
        full and the Producer will have to wait before retrying it.
        ! The Producer must function endlessly, thus recalling its
        own run() method after the initial iteration.
        """

        for product in self.products:
            quantity = product[1]
            while quantity:
                if self.marketplace.publish(
                        self.marketplace.register_producer(),
                        product[0]):
                    quantity -= 1
                    time.sleep(product[2])
                    continue
                time.sleep(self.republish_wait_time)
        self.run()
