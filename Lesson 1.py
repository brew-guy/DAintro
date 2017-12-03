# Iterables have __iter__ functions in them
# Iterators make use of the next method to move from element to element within their associated iterable
def myforloop(anyiterable):
    my_iterator = anyiterable.__iter__()
    while True:
        try:
            print my_iterator.next()
        except StopIteration:
            break

myforloop([1,2,3])


