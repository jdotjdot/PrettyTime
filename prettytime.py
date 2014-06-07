import datetime
from operator import itemgetter
from dateutil.relativedelta import *

class NegativeError(ValueError): pass

class t(object):

  TIME_LIST = ['seconds', 'minutes', 'hours', 'days', 'weeks',
                'months', 'years']
  EXPANDED_TIME_LIST = TIME_LIST + map(itemgetter(slice(None, -1)), TIME_LIST)

  def __init__(self, num):
    if num >= 0:
      self.num = num
    else:
      raise NegativeError("Cannot accept negative values.  Use 'ago' to go back in time.")

  def _make(self, timedict):
    return PrettyDelta(**timedict)

  def __getattr__(self, attr):
    attr = attr.lower()
    if attr not in self.EXPANDED_TIME_LIST:
      raise AttributeError("Attribute '{}' not found.".format(attr))
    else:
      if not attr[-1] == ('s'):
        attr += 's'
      return self._make({attr: self.num})

class PrettyDelta(relativedelta):

  def _order(self):
    smalltime = ['seconds', 'minutes', 'hours']
    if all([getattr(self, item)==0 for item in smalltime]):
      return datetime.date
    else:
      return datetime.datetime

  @property
  def ago(self):
    return self._order().today() - self

  @property
  def from_now(self):
    return datetime.datetime.today() + self

  @property
  def from_today(self):
    return datetime.date.today() + self