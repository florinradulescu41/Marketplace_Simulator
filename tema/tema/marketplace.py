"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock, currentThread
from tema.product import Product

class Marketplace:
    """
    Class that represents the Marketplace.
    It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """ Constructor.
        queue_size_per_producer: int -- the maximum size of the
                            queue associated with each Producer;
        Attributes:
        buffer: set() -- the shared space of the Marketplace,
                contains all products from all the Producers;
        producers: list where producer[k]=number of products
                    of the k_th producer currently in buffer;
        products: maps Products with the id of their Producers;
        carts: maps the cart_id with a list of Products inside;
        Locks:
        queue_size_lock: for modifying producers[producer_id]
                (more Consumers can't take the same Product);
        carts_lock: for modifying carts_number
            (more Consumers should not receive the same carts);
        """

        self.queue_size_per_producer = queue_size_per_producer
        self.buffer = set()
        self.producers = [int] # must be protected with a lock
        self.products = {Product: int}  # Product: producer_id
        self.carts = {int: [Product]} # cart_id: list[Product]
        self.carts_number = 0  # must be protected with a lock

        self.size_lock = Lock()     # protects self.producers
        self.carts_lock = Lock()    # protects self.carts_number

    def register_producer(self):
        """ Returns an id (int) for the producer that calls this. """

        self.producers.append(0)    # add a new Producer with 0 Products
        return len(self.producers) - 1  # Producer[k] should have id = k

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the Marketplace.
        producer_id: int -- producer id; (was unnecessarily a String)
        product: Product -- a Product to be published in Marketplace;
        Returns True or False.
        If the caller receives False, it should wait and then try again.
        """

        if self.producers[producer_id] >= self.queue_size_per_producer:
            return False
        self.products[product] = producer_id
        self.producers[producer_id] += 1
        self.buffer.add(product)
        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer.
        Returns an int representing the cart_id.
        A Lock is used so just one Thread increments the carts_number.
        """

        with self.carts_lock:
            self.carts_number += 1
        self.carts[self.carts_number] = []
        return self.carts_number

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart.
        cart_id: int -- cart where the add operation is executed;
        product: Product -- the product to be added to cart;
        Returns True or False.
        If the caller receives False, it will wait before a retrying.
        The Product must be in the Marketplace to be added.
        It will not be in the Marketplace anymore after an operation.
        A Lock is needed, more Consumers can't take the same Product.
        """

        if product in self.buffer:
            with self.size_lock:
                self.producers[self.products[product]] -= 1
            self.buffer.discard(product)
        else:
            return False
        self.carts[cart_id].append(product)
        return True

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        cart_id: int -- cart where the remove operation is executed;
        product: Product -- the product to be removed from cart;
        The Product must be in the cart to be removed.
        It will move in the Marketplace after the operation, in its
        previous list of Products from a Producer. In order to call
        an increment on the list, a Lock is needed.
        """

        if product in self.carts[cart_id]:
            self.carts[cart_id].remove(product)
            self.buffer.add(product)
            with self.size_lock:
                self.producers[self.products[product]] += 1

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.
        cart_id: int -- cart id from where the Products are ordered;
        In order to make safe prints inside Threads, a Lock in used.
        """

        prod_list = self.carts.pop(cart_id) # type = List[Product]
        for product in prod_list:
            print(currentThread().getName() + " bought " + str(product))
