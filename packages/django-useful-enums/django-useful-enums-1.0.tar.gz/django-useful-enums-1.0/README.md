# Useful Enums - a library for creating Enums in a DRY way in Python

[![Build
Status](https://travis-ci.org/grahambinns/django-useful-enums.png?branch=master)](https://travis-ci.org/grahambinns/django-useful-enums)

This library grew out of me getting fed up with having to create Django
choices that were lists of tuples. I far preferred nicely contained enums of
the form:

    class MyEnum:

        VALUE_1 = 1
        VALUE_2 = 2

However, most of the time you don't _need_ to create all of the IDs yourself.
You should just be able to define the key names and have the Enum class do the
work for you. `usefulenums` does that.

The syntax is very similar to the Django idiom for creating a tuple of choices:

    from usefulenums import Enum

    MyEnum = Enum(
        ("MY_FIRST_VALUE", "My First Display Text"),
        ("MY_SECOND_VALUE", "My Second Value"),
    )

However, you can now refer to those items by name in a more Pythonic fashion,
rather than having to use hard-coded strings:

    >>> MyEnum.MY_FIRST_VALUE
    0

Note that here, `Enum()` has given automatic values to the enum items. You can
set these values yourself by passing a three-tuple to `Enum` when you create
it:

    >>> MyEnum = Enum(
    ...     ("VALUE_1", "MY_FIRST_VALUE", "My First Value"),
    ...     ("VALUE_2", "MY_SECOND_VALUE", "My Second Value"),
    ... )
    >>> print(MyEnum.MY_FIRST_VALUE)
    VALUE_1

You can also extract the Django-style choices from the `Enum` so that you use
it as you've always used choices:

    >>> MyEnum.as_choices()
    (('VALUE_1', 'My First value'), ('VALUE_2', 'My Second Value'))


# Testing

`django-useful-enums` comes with unit tests that cover its behaviour. You can
run them using `nose`:

    $ pip install nose
    $ nosetests
