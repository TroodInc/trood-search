Querying
===========

Index table
-----------

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 1  | Men shorts    | pants  | 50    |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+

Simple
------

All fields
__________

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=shorts&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 1  | Men shorts    | pants  | 50    |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+

By field
________

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=@type shorts&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+

NOT
---

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=-pants&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+

AND
---

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=@product shorts @type shorts&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+


OR
--

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=(@product shorts | @type pants)&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 1  | Men shorts    | pants  | 50    |
+----+---------------+--------+-------+
| 2  | Women shorts  | shorts | 100   |
+----+---------------+--------+-------+
| 3  | Unisex shorts | shorts | 75    |
+----+---------------+--------+-------+

OR and AND together
-------------------

.. code-block:: bash

    curl -X GET 'http://search-host/?index=index&match=(@product shorts | @type pants) @price 50&limit=0,100'

+----+---------------+--------+-------+
| id | product       | type   | price |
+----+---------------+--------+-------+
| 1  | Men shorts    | pants  | 50    |
+----+---------------+--------+-------+

Links
-----

* `Sphinx HTTP protocol feature <http://sphinxsearch.com/blog/2016/10/12/2-3-2-feature-http-protocol/>`_.
* `Sphinx extended query syntax <http://sphinxsearch.com/docs/current/extended-syntax.html>`_.
