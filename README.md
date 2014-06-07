PrettyTime
==========

Python PrettyTime - A Python module allowing Rails-style pretty times like t(3).days.ago
--------

Version 0.0.1a

PrettyTime is a small Python package that intends to create a better interface for working with dates and times in Python.  It was inspired by Rails' syntax for dates and times, like:

```ruby
3.days.ago
2.hours.from_now
```

Though Python does not allow the same type of built-in monkey-patching, you can get decently close.  PrettyTime currently offers the following:

```python
>>> t(4).hours.from_now
datetime.datetime(2014, 6, 7, 3, 51, 51, 422545)
>>> t(1).years.from_today
datetime.date(2015, 6, 6)
```

## Usage

### Download
For now, clone the [GitHub repository](https://github.com/jdotjdot/PrettyTime):

    git clone https://github.com/jdotjdot/PrettyTime

Later releases will be uploaded to `pip`.

### Import

    from prettytime import t

### Use

Because you can't override Python literals, all integers must be wrapped by `t()`.  Everything else tries to be normal English.

Commands currently supported:

Date/Time   | Relative
------------|----------
`second(s)` | `ago`
`minute(s)` | `from_now`
`hour(s)`   | `from_today`
`day(s)`    |
`week(s)`   |
`month(s)`  |
`year(s)`   |

## Planned changes:

 + Change the `.from_now` and `.from_today` methods to separate `.from` and `.today`/`now` methods to allow for a variety of endings:
     * `.from.today`
     * `.from.tomorrow`
     * `.from.next_year`
     * ...etc.
 + Add [`django-pretty-times`](https://pypi.python.org/pypi/django-pretty-times/0.1.0)-like functionality to allow pretty printing as well