.. image:: https://travis-ci.org/eblade/jsonobject.svg?branch=master
    :target: https://travis-ci.org/eblade/jsonobject

.. image:: https://img.shields.io/pypi/v/lindh-jsonobject.svg
    :target: https://pypi.python.org/pypi/lindh-jsonobject/

.. image:: https://img.shields.io/pypi/l/lindh-jsonobject.svg
    :target: https://pypi.python.org/pypi/lindh-jsonobject/

.. image:: https://codecov.io/gh/eblade/jsonobject/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/eblade/jsonobject


lindh-jsonobject
================

JSON serializable python3 objects.

Introduction
------------

The purpose with ``lindh.jsonobject`` is to provide a way to serialize and
deserialize python3 objects into and from JSON so that they can be communicated
with other application and stored into document databases such as CouchDB.

Some code and inspiration comes from the Django project, and the objects behave
much like such. However, while Django objects are meant for relational databases,
these are meant to be used with complex objects in document databases.

Dependencies
------------

There are no dependencies besides core python3.7+

Installation
------------

This repository can be installed with ``pip``.

.. code-block:: bash

    pip install lindh-jsonobject

Example
-------

.. code-block:: python

    >>> from json import dumps
    >>> from lindh.jsonobject import Property, PropertySet, EnumProperty

    >>> class Wheel(PropertySet):
    ...    diameter = Property(float, default=1.)

    >>> class Rating(EnumProperty):
    ...    ok = 'ok'
    ...    bad = 'bad'
    ...    good = 'good'

    >>> class Car(PropertySet):
    ...    wheels = Property(type=Wheel, is_list=True)
    ...    brand = Property()
    ...    model = Property()
    ...    rating = Property(enum=Rating, default=Rating.ok)

    >>> volvo = Car(brand='Volvo', model='V70', rating=Rating.good)
    >>> print(volvo.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V70",
      "rating": "good",
      "wheels": []
    }

    >>> volvo.wheels.append(Wheel(diameter=2.))
    >>> print(volvo.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V70",
      "rating": "good",
      "wheels": [
        {
          "*schema": "Wheel",
          "diameter": 2.0
        }
      ]
    }

    >>> volvo.wheels.append(Wheel(diameter=2.))
    >>> print(volvo.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V70",
      "rating": "good",
      "wheels": [
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 2.0
        }
      ]
    }

    >>> volvo.wheels.append(Wheel(diameter=2.))
    >>> volvo.wheels.append(Wheel())  # using default value here
    >>> print(volvo.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V70",
      "rating": "good",
      "wheels": [
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 1.0
        }
      ]
    }

    >>> volvo2 = Car.FromJSON(volvo.to_json())
    >>> print(volvo2.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V70",
      "rating": "good",
      "wheels": [
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 2.0
        },
        {
          "*schema": "Wheel",
          "diameter": 1.0
        }
      ]
    }


Type Hinting
------------

You can also specify types for properties with Type Hinting, if available:

.. code-block:: python

    >>> from json import dumps
    >>> from typing import List
    >>> from lindh.jsonobject import Property, PropertySet, EnumProperty

    >>> class Wheel(PropertySet):
    ...    diameter: float = Property(default=1.)

    >>> class Rating(EnumProperty):
    ...    ok = 'ok'
    ...    bad = 'bad'
    ...    good = 'good'

    >>> class Car(PropertySet):
    ...    wheels: List[Wheel] = Property()
    ...    brand = Property()
    ...    model = Property()
    ...    rating: Rating = Property(default=Rating.ok)

    >>> volvo = Car(brand='Volvo', model='V90', rating=Rating.good, wheels=[])
    >>> volvo.wheels.append(Wheel(diameter=3.))
    >>> print(volvo.to_json())
    {
      "*schema": "Car",
      "brand": "Volvo",
      "model": "V90",
      "rating": "good",
      "wheels": [
        {
          "*schema": "Wheel",
          "diameter": 3.0
        }
      ]
    }


Supported types:

  * ``str``
  * ``int``
  * ``float``
  * ``bool``
  * ``dict``
  * ``typing.List[T]`` where ``T`` is a subclass of ``PropertySet``
  * ``T`` where ``T`` is a subclass of EnumProperty


Schema-Less
-----------

There is also included a "schema-less" mode, found under
``lindh.jsonobject.noschema``. The idea is to provide an easy-to-use read-only
LINQ-like way of exploring JSON-like files. Here is a small example:

.. code-block:: python

    >>> from lindh.jsonobject import Dictionary
    >>> d = Dictionary.load('tests/test.json')
    >>> palle = (d.drivers
    ...     .where(lambda x: x.name == "Palle Kuling")
    ...     .join(d.cars, lambda driver, car: driver.car_brand == car.brand and driver.car_model == car.model)
    ...     .single())
    >>> palle.rating
    'good'


You can also use chained methods like ``select(expr)``, ``first()`` and ``extend(**items)``.


Author
------

``lindh.jsonobject`` is written and maintained by Johan Egneblad <johan@egneblad.se>.
