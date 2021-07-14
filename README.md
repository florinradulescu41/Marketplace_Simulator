# Marketplace
Producer-Consumer Multithreading



Organization

Within this theme we have implemented a Marketplace model through which more
manufacturers can offer their products for sale, and more buyers can purchase
the products made available.
The manufacturers will be identified as Producers and the buyers as Consumers.

Marketplace

The Marketplace is a class that contains a common buffer with two types of
Products (tea and coffee) that are marketed by the Producers.
This is the intermediary between Producers and Consumers, through which the
purchase of products is made:
- the Producer produces a certain quantity of products of one / more types
- the Consumer buys a certain quantity of products of one / more types
The Marketplace also provides each Consumer with a basket of products (cart)
(this will be used to reserve the products that are to be bought).

Producer

There are several Producers that produce coffee / tea items, called Products.
Each Product will be supplied in a certain quantity. A Producer can produce
both coffee and tea items.

Consumer

When a Consumer wants to buy certain Products from the store, he will need a
shopping cart to use in order to reserve them. Thus, every time a Consumer
starts shopping, he will receive a shopping cart from the Marketplace, which
will be associated with an id. The Consumer can:
- add products to cart ⇒ those Products become unavailable to other Consumers
- delete products from the cart ⇒ those Products become available again
- place an order


Explanation for the chosen solution:

In order to store and access the data in the files efficiently from a temporal
point of view, the main buffer in the Marketplace was implemented using a set.
The operations used by add and discard on the set are thread-safe and do not
require synchronization means.

The Producers are kept in a list in which the index is the Producer's id, and
the value is the number of Products that the Producer has in the buffer.
This makes it easy to add Producers through the thread-safe append method and
thus the registration is done without synchronization elements. However, they
will have to be used to change the quantity of Products in the list, which must
be executed safely in order to always be able to see if there is room for a new
Product or if the Producer has to wait before another publish attempt in the
Marketplace.

The Products in the buffer are also kept in a dictionary that contains as a key
an object of Product type and as a value the id of its Producer. This particular
implementation was chosen to be able to easily modify the Product lists of each
Producer when a Consumer performs operations on Products.

A dictionary is also used to store all Consumers' carts. There each cart will be
identified by the id and it will have associated the list of Products inside it.
This implementation facilitates the thread-safe operations on the Products in the
cart, namely append/remove and extracting the entire list for placing the order.

We tried to use the synchronization elements as efficiently as possible, which
is why many structures with thread-safe operations were used. However, they did
not work anywhere, and two locks were needed to protect the critical areas like
the number of Products in the list of Producers or in number of carts.
However, in some cases the use of the dictionary at the expense of a list has
been somewhat forced by the lack of effective methods to access safe items.
It will be noted that the use of locks is restricted each time to a single
critical operation applied on the dictionaries. An implementation with lists only
would have generated more operations under the incidence of locks, thus overhead.

Skeleton modifications:

Although no function header was changed, the comments in the skeleton mentioned
the producer_id attribute in the publish method as String, which seemed a bit
inefficient. This is because the register returns an int in the Producer class,
which then calls the publish method using the received int id as String, which
would only generate unnecessary conversions. As a result, a Producer's id is
treated as int throughout the entire implementation.

Interesting observation:

An unexpected thing was that the printouts did not need a lock to pass the tests
(initially each Thread that prints called an assigned lock). I don't know if this
is a particular property of the following tests. I did not generate my own tests,
but I suspect there might be some cases is which the unsecured prints ("could")
create some undesired behaviour of the application.

Resources used

The development used both the notions acquired in ASC laboratories and some
additional notions discovered on the Internet, mostly related to how certain
data structures work in parallel computing using Python.
In this sense, information from the following sites was used:
https://data-flair.training/blogs/python-data-structures-tutorial/
https://www.datacamp.com/community/tutorials/sets-in-python
https://stackoverflow.com/questions/2831212/
