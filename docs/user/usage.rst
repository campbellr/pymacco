.. _usage:

Usage
=====

.. note:: 
    The usage described here is more of a design guide, since nothing
    has actually been implemented yet.

.. note::
    At some point there may be multiple interfaces (command-line, web, GTK, mobile, etc...) but
    this guide currently only describes the command-line interface.

Connecting to a Server
----------------------

Whether you want to create a new game or join an existing game, you're going
to want to first connect to a server.

.. note:: For information on hosting your own pymacco server, read on.

To connect to a ``pymacco`` server either use the ``--server`` argument when
starting ``pymacco``, or use the ``connect`` command: ::

    $ pymacco --server <address_of_server>
    pymacco version 0.1
    Type 'help' for a list of available commands.
    Connected to server <server>. 
    >>>

Alternatively, you can use the ``connect`` command: ::

    $ pymacco
    pymacco version 0.1
    Type 'help for a list of available commands.
    >>> connect <address_of_server>
    Connected to server <server>
    >>>
 

Joining an Existing Game
------------------------

Creating a New Game
-------------------

Playing a Game
--------------



