PrettyTime
==========

Version 0.0.1a

PrettyTime is a small Python package that intends to create a better interface for working with dates and times in Python.  It was inspired by Rails' syntax for dates and times, like:

```ruby
3.days.ago
2.hours.from_now
```

Though Python does not allow the same type of built-in monkey-patching, you can get decently close.  An example of what PrettyTime currently offers:

```python
>>> t(4).hours.from_.now
datetime.datetime(2014, 6, 7, 3, 51, 51, 422545)
>>> t(1).years.from_.today
datetime.date(2015, 6, 6)
```

## Usage

### Download
Install from PyPI:

    pip install prettytime

Alternatively, you can clone the [GitHub repository](https://github.com/jdotjdot/PrettyTime):

    git clone https://github.com/jdotjdot/PrettyTime

### Import

    from prettytime import t

### Use

Because you can't override Python literals, all integers must be wrapped by `t()`.  Everything else tries to be normal English.

Commands currently supported:

Date/Time   | Relative |               |
------------|----------|---------------|------------
`second(s)` | `ago`    | `next`        | `week`
`minute(s)` | `from_`  | `last`        | `month`
`hour(s)`   | `before` |  `now`        | `year`
`day(s)`    | `after`  | `today`       |
`week(s)`   |          |  `tomorrow`   |
`month(s)`  |          |  `yesterday`  |
`year(s)`   |          |               |

Examples:

```python
>>> from prettytime import *
>>> t(3).days.from_.next.year
datetime.date(2015, 6, 15)
>>> t(4).years.ago
datetime.date(2010, 6, 12)
>>> t(10).months.before.last.week
datetime.date(2013, 8, 5)
>>> t(7).minutes.after.tomorrow
datetime.datetime(2014, 6, 13, 23, 57, 44, 38401)
```

## Planned changes:

 + Add [`django-pretty-times`](https://pypi.python.org/pypi/django-pretty-times/0.1.0)-like functionality to allow pretty printing as well