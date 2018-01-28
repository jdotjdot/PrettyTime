import calendar
import datetime
from operator import itemgetter, neg, pos
from dateutil.relativedelta import *

TIME_LIST = ['seconds', 'minutes', 'hours', 'days', 'weeks', 'months', 'years']
LOWER_TIME_LIST = list(map(itemgetter(slice(None, -1)), TIME_LIST))
EXPANDED_TIME_LIST = TIME_LIST + LOWER_TIME_LIST

class NegativeError(ValueError): pass


def expanddelta(function):
    def wrapper(*args):
        not_allowed_list = ['_has_time']
        rd = function(*args)
        return expandeddelta(**{key: value for key, value in rd.__dict__.iteritems() if key not in not_allowed_list})
    return wrapper

class expandeddelta(relativedelta, object):

    def __pos__(self):
        return self

    @expanddelta
    def __neg__(self):
        return super(expandeddelta, self).__neg__()

    # Necessary to cover for relativedelta's use of singular year, month, etc. in __radd__
    def __add__(self, other):
        if isinstance(other, relativedelta):
            return relativedelta(years=other.years+self.years,
                                 months=other.months+self.months,
                                 days=other.days+self.days,
                                 hours=other.hours+self.hours,
                                 minutes=other.minutes+self.minutes,
                                 seconds=other.seconds+self.seconds,
                                 microseconds=other.microseconds+self.microseconds,
                                 leapdays=other.leapdays or self.leapdays,
                                 year=other.year or self.year,
                                 month=other.month or self.month,
                                 day=other.day or self.day,
                                 weekday=other.weekday or self.weekday,
                                 hour=other.hour or self.hour,
                                 minute=other.minute or self.minute,
                                 second=other.second or self.second,
                                 microsecond=other.microsecond or self.microsecond)
        if not isinstance(other, datetime.date) and type(other) is not t:
            raise TypeError("unsupported type for add operation")
        elif self._has_time and not isinstance(other, datetime.datetime):
            other = datetime.datetime.fromordinal(other.toordinal())
        year = (other.year if other.year else 0)+self.years
        month = other.month if other.month else 0
        if self.months:
            assert 1 <= abs(self.months) <= 12
            month += self.months
            if month > 12:
                year += 1
                month -= 12
            elif month < 1:
                year -= 1
                month += 12
        day = min(calendar.monthrange(year, month)[1],
                  other.day)
        repl = {"year": year, "month": month, "day": day}
        # for attr in ["hour", "minute", "second", "microsecond"]:
        #     value = getattr(self, attr)
        #     if value is not None:
        #         repl[attr] = value
        days = self.days
        if self.leapdays and month > 2 and calendar.isleap(year):
            days += self.leapdays
        ret = (other.replace(**repl)
               + datetime.timedelta(days=days,
                                    hours=self.hours,
                                    minutes=self.minutes,
                                    seconds=self.seconds,
                                    microseconds=self.microseconds))
        if self.weekday:
            weekday, nth = self.weekday.weekday, self.weekday.n or 1
            jumpdays = (abs(nth)-1)*7
            if nth > 0:
                jumpdays += (7-ret.weekday()+weekday)%7
            else:
                jumpdays += (ret.weekday()-weekday)%7
                jumpdays *= -1
            ret += datetime.timedelta(days=jumpdays)
        return ret


class DeltaMixin(object):
    def _order(self):
        smalltime = ['seconds', 'minutes', 'hours']
        if all([getattr(self, item) == 0 for item in smalltime]):
            return datetime.date
        else:
            return datetime.datetime

class t(object):
    TIME_LIST = TIME_LIST
    EXPANDED_TIME_LIST = EXPANDED_TIME_LIST

    def __init__(self, num=None):
        if num is not None:
            if num >= 0:
                self.num = num
            else:
                raise NegativeError("Cannot accept negative values.  Use 'ago' to go back in time.")
        else:
            self.num = None
            self.today = datetime.datetime.today()

    def _make(self, timedict):
        return PrettyDelta(**timedict)

    def __getattr__(self, attr):
        attr = attr.lower()
        if self.num is not None:
            if attr not in self.EXPANDED_TIME_LIST:
                raise AttributeError("Attribute '{}' not found.".format(attr))
            else:
                if not attr[-1] == ('s'):
                    attr += 's'
                return self._make({attr: self.num})
        else:
            return getattr(self.today, attr)

    def __repr__(self):
        if self.num is None:
            return self.today.__repr__()
        else:
            super(t, self).__repr__()

    def __str__(self):
        if self.num is None:
            return self.today.__str__()
        else:
            return super(t, self).__str__()

class PrettyDelta(expandeddelta, DeltaMixin):

    @property
    def ago(self):
        return self._order().today() - self

    def get_delta2(self, direction):
        # direction is operator.pos or operator.neg
        return PrettyDelta2(order=self._order(), **direction(self).__dict__)

    @property
    def From(self):
        return self.get_delta2(pos)
    from_ = From
    after = From

    @property
    def before(self):
        return self.get_delta2(neg)
    Before = before

    @property
    def in_(self):
        return
    In = in_

class PrettyDelta2(expandeddelta, DeltaMixin):

    # Will make calculation with (magnitude, order, direction, [magnitude, order, direction])

    relativedict = {
        'next': pos,
        'last': neg,
    }

    timedict = {
        'today': expandeddelta(),
        'now': expandeddelta(),
        'tomorrow': expandeddelta(days=1),
        'yesterday': expandeddelta(days=-1),
    }

    def _self(self):
        return self

    def __init__(self, *args, **kwargs):
        # self.direction = kwargs.pop('direction')
        self.order = kwargs.pop('order')
        self._minidirection = pos
        self._minidirection_count = 0
        if '_has_time' in kwargs:
            del kwargs['_has_time']
        super(PrettyDelta2, self).__init__(*args, **kwargs)
        for thing in LOWER_TIME_LIST:
            if thing in self.__dict__:
                del self.__dict__[thing]

    def dt(self, time=False):
        return datetime.datetime if time else datetime.date

    def then(self, date):
        return self + date

    def __getattr__(self, item):

        item = item.lower()

        # if 'last' or 'next'
        if item in self.relativedict:
            if self._minidirection_count:
                # already called last or next
                raise SyntaxError("Attempted to call 'last' or 'next' more than once")
            else:
                self._minidirection = self.relativedict[item]
                self._minidirection_count += 1
                return self

        elif item == 'then':
            return self.then

        # `self` MUST appear on the left side of the addition
        elif item in self.timedict:
            if item == 'now':
                return self + datetime.datetime.today() + self._minidirection(self.timedict[item])
            else:
                return self + self.order.today() + self._minidirection(self.timedict[item])

        elif item in EXPANDED_TIME_LIST:
            if not item[-1] == 's':
                item += 's'
            return self + self.order.today() + self._minidirection(expandeddelta(**{item: 1}))

        else:
            super(PrettyDelta2, self).__getattribute__(item)
