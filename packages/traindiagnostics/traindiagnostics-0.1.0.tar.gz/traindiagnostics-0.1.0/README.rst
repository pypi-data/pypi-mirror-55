================
traindiagnostics
================

A Python library for unevenly-spaced time series analysis in train diagnostics.
Build on top of the magnificent `ticts <https://github.com/gjeusel/ticts>`_ library.


Installation
------------

.. code:: bash

    pip install traindiagnostics


Usage
-----

.. code:: python

    import traindiagnostics as td
    ts = td.TimeSeries({
        '2019-01-01 09:00:00': 0,
        '2019-01-01 09:00:05': 1,
        '2019-01-01 09:01:02': 0,
        '2019-01-01 09:05:09': 1,
        '2019-01-01 09:05:16': 0,
        '2019-01-01 09:11:01': 1,
        '2019-01-01 09:12:59': 0,
    })

   not_in_index = '2019-01-01 00:05:00'
   assert ts[not_in_index] == 1  # step function, previous value

   ts['2019-01-01 00:04:00'] = 10
   assert ts[not_in_index] == 10

   assert ts + ts == 2 * ts

   ts_evenly_spaced = ts.sample(freq='1Min')

   # From ticts to pandas, and the other way around
   assert ts.equals(
      ts.to_dataframe().to_ticts(),
   )

Contributing
------------

Missing some features? create an issue or pull request!
