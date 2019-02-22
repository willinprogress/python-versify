Quickstart
==========

Eager to get started? This page gives a good introduction in how to get started with versify.

First, make sure that:

- Versify is `installed`_
- you have a file ``config.ini`` with this content:

.. code:: ini

   [dbt]
   key = myDbtKey
   lang = FRN

.. _installed: install.html

Let’s get started with some simple examples.

Get a verse on bible
--------------------

Get a verse with versify is very simple.

Begin by importing the versify module:

.. code:: python

   from versify.util.Dbt import Dbt

Now, let’s try to get a verse.

.. code:: python

   # locate the config.ini file
   dbt = Dbt(config_path="/path/to/config.ini")

   # DBY is the code of Darby
   print(dbt.find_verse("DBY", "1 Timothée", 2, 1))


That’s all well and good, but it’s also only the start of what versify can do.


Get List of verse of chapters
-----------------------------

You often want to get all the verse of chapter on bible. You would use the following code.

.. code:: python

   # locate the config.ini file
   dbt = Dbt(config_path="/path/to/config.ini")

   # DBY is the code of Darby
   print(dbt.find_chapters("DBY", "1 Timothée", 2).get_verses(dbt))



Get random verse on bible
-------------------------


You often want to get a random verse on bible. You would use the following code.

.. code:: python

   # locate the config.ini file
   dbt = Dbt(config_path="/path/to/config.ini")

   # DBY is the code of Darby
   print(dbt.get_random_verse("DBY"))
