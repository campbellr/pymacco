.. _style:

Style Guide
===========

Since this project uses Twisted_, all code should comply with the
`Twisted coding standards`_ for consistency.

In brief, that mostly means:

.. rubric:: StudlyCaps for class names

From the guide:

    Classes are to be named in mixed case, with the first letter capitalized;
    each word separated by having its first letter capitalized. *Acronyms
    should be capitalized in their entirety*. Class names should not be
    prefixed with the name of the module they are in.

.. rubric:: Method/function names should be mixed case

From the guide:

    Methods should be in mixed case, with the first letter lower case,
    each word separated by having its first letter capitalized.
    For example, ``someMethodName``, ``method``.

    Sometimes, a class will dispatch to a specialized sort of method using
    its name; for example, ``twisted.reflect.Accessor``. In those cases,
    the type of method should be a prefix in all lower-case with a trailing
    underscore, so method names will have an underscore in them. For example,
    ``get_someAttribute``. Underscores in method names in twisted code are
    therefore expected to have some semantic associated with them.


.. _Twisted: http://twistedmatrix.com
.. _Twisted coding standards: http://twistedmatrix.com/documents/current/core/development/policy/coding-standard.html
