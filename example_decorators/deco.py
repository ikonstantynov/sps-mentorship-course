import functools


def say_hello(name):
    return f"Hello {name}"


def be_awesome(name):
    return f"Yo {name}, together we are the awesomest!"


def greet_bob(greeter_func):
    return greeter_func("Bob")


print(greet_bob(say_hello))
print(greet_bob(be_awesome))


def deco(fun):
    def wrapper(*args, **kwargs):
        print(fun.__name__, args, kwargs)
        return fun(*args, **kwargs)
    return wrapper


def new_deco(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        print(fun.__name__, args, kwargs)
        return fun(*args, **kwargs)
    return wrapper


def twice(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        print(fun.__name__, args, kwargs)
        result = fun(*args, **kwargs)
        return result * 2
    return wrapper


def add_100(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        print(fun.__name__, args, kwargs)
        result = fun(*args, **kwargs)
        return result + 100
    return wrapper


first, *rest = range(1, 5)
print(first, rest)

first, *_, last = [2, 3, 4, 5]
print(first, last)


@deco
def add(x, y):
    """ Doc string """
    return x+y


@new_deco
def mul(x, y):
    """Doc string"""
    return x*y


@add_100
@twice
def something(x):
    return x


print(add(1, 2))
print(add.__doc__)

print(mul(2, 3))
print(mul.__doc__)

print(something(4))


# Contracts For Python
# https://pypi.org/project/contracts/

# https://docs.python.org/3/library/functools.html


@functools.lru_cache(maxsize=2)
def cache(x):
    print('Call')
    return x * 2

print(cache(2))
print(cache(2))
print(cache(3))
print(cache(3))
print(cache(4))
print(cache(4))
print(cache(4))
print(cache(2))

print(cache.cache_info())

# partial

def add(x, y):
    return x + y


p_add = functools.partial(add, 2)
print(p_add(4))


# singledispatch

@functools.singledispatch
def add(a, b):
    print("Not Implemented")


@add.register(int)
def _(a, b):
    print("For int")
    print(a + b)


@add.register(str)
def _(a, b):
    print("For string")
    print(a + b)


add(1, 2)
add('a', 'b')
add([1, 2], [2, 3])
