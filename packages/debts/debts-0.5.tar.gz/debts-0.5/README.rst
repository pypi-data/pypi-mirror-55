Debts settlement
================

A simple library and cli-tool to help you solve some debts settlement scenarios.

Installation
------------

From a command-line interface, run::

        $ pip install debts

From the command-line
---------------------

You can invoke the solver from the command-line. To do so, you need to pass it
the arguments in a specific way::

        $ debts --settle "Emeline -200, Alexis -400, Rémy +500, Alexis +100"
        Emeline → Rémy: 200.0
        Alexis → Rémy: 300.0

You can also read from a JSON file::

        $ debts --settle data.json --parser=json

And optionally render a HTML table with the results::

        $ debts --settle data.json --parser=json --renderer=html > index.html

Which should look like this:

.. image:: screenshots/html-output.png

As a library
------------

If you want to use it as a library, here is how it works::

        >>> from debts import settle
        >>> settle([('Emeline', -200), ('Alexis', -400), ('Rémy', +500), ('Alexis', +100)])
        [('Emeline', 200.0, 'Rémy'), ('Alexis', 300.0, 'Rémy')]

That's all folks!

Testing
-------

Everything is tested and should work. If it doesn't, please take the time to
open an issue here! Thanks :-)

To run the tests yourself::

  $ pip install -e .
  $ pip install -r dev-requirements.txt
  $ py.test tests
