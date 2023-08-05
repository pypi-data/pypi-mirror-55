*******
Example
*******

You can represent a binary tree in a simple flat list using the following structure.

.. code-block:: python

    """

         3
     1       5
   0   2   4   6  ...

   """

This module exposes a series of functions to help you build and maintain this data structure.

.. code-block:: python

    from flat_tree import FlatTreeAccessor

    tree_access = FlatTreeAccessor()
    tree_access.index(1, 0)  # get index @ depth: 1, offset: 0
