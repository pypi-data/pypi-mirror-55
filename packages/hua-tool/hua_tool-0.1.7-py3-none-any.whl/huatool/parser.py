import huatool as HT

def toOneHot(num_classes, indexes):
    '''One Hot'''
    return HT.Numpy.eye(num_classes)[indexes]

def bytesToUTF8(data):
    '''把 bytes 字串，转换成 utf-8 字串'''
    if isinstance(data, bytes): return data.decode('utf-8')
    if isinstance(data, dict): return dict(map(bytesToUTF8, data.items()))
    if isinstance(data, tuple): return [bytesToUTF8(v) for v in data]
    return data

def sourceCode(funct):
    '''获取函数原始码'''
    return Inspect.getsourcelines(funct)

def strToFunct(string):
    '''将字符串函数转成可使用的函数'''
    code = compile(string, '', 'exec')
    return HT.FunctionType(code.co_consts[0], globals())

class ParseDateStringException(Exception):
    '''解析日期错误'''
    def __init__(self, string):
        super().__init__(string)
        self.string = string

class Date(object):
    '''日期类（可传入毫秒、日期字串、本身、datetime）'''
    def __init__(self, date_str=None):
        if date_str is None:
            self.DateTime = HT.DateTime.datetime.now()
        elif type(date_str) == HT.DateTime.datetime:
            self.DateTime = date_str
        elif type(date_str) == Date:
            self.DateTime = date_str.DateTime
        else:
            try:
                self.DateTime = HT.DateUtilParser.parse(date_str)
            except:
                try:
                    self.DateTime = HT.DateUtilParser.parse(HT.Time.ctime(int(date_str) / 1000.0))
                except:
                    raise ParseDateStringException(date_str)

    def addDay(self, delta):
        '''加减天数'''
        return Date(Date.dateTimeDelta(self.DateTime, deltatype="day", delta=delta))

    def addWeek(self, delta):
        '''加减星期'''
        return Date(Date.dateTimeDelta(self.DateTime, deltatype="week", delta=delta))

    def addMonth(self, delta):
        '''加减月数'''
        return Date(Date.dateTimeDelta(self.DateTime, deltatype="month", delta=delta))

    def addYear(self, delta):
        '''加减年数'''
        return Date(Date.dateTimeDelta(self.DateTime, deltatype="year", delta=delta))

    def add(self, deltatype, delta):
        '''加减'''
        return Date(Date.dateTimeDelta(self.DateTime, deltatype=deltatype, delta=delta))

    def toString(self, year=True, month=True, day=True, bar=True, sep='-'):
        '''日期字串'''
        result = ""
        if year:
            result += "%04d" % self.DateTime.year
        if month:
            if bar and result != "":
                result += sep
            result += "%02d" % self.DateTime.month
        if day:
            if bar and result != "":
                result += sep
            result += "%02d" % self.DateTime.day
        return result

    @staticmethod
    def between(start, end):
        '''两个日期间的所有日期（包含始末）'''
        start = Date(start)
        end = Date(end)
        if start.string > end.string:
            start, end = end, start
        for i in range(end - start + 1):
            yield start.addDay(i)

    @property
    def unixtimems(self):
        '''unix timestamp 毫秒级别'''
        return int(HT.Time.mktime(self.DateTime.timetuple()) * 1000)

    @property
    def string(self):
        '''简单的日期字串'''
        return self.toString()
    
    @property
    def year(self):
        '''年份'''
        return self.DateTime.year

    @property
    def month(self):
        '''月份'''
        return self.DateTime.month
    
    @property
    def day(self):
        '''日'''
        return self.DateTime.day

    @property
    def yearStr(self):
        '''年份字串，格式为 %04d'''
        return "%04d" % self.DateTime.year

    @property
    def monthStr(self):
        '''月份字串，格式为 %02d'''
        return "%02d" % self.DateTime.month
    
    @property
    def dayStr(self):
        '''日字串，格式为 %02d'''
        return "%02d" % self.DateTime.day

    @property
    def weekyear(self):
        '''周的年份'''
        return self.DateTime.isocalendar()[0]

    @property
    def weeknum(self):
        '''今年第几周'''
        return self.DateTime.isocalendar()[1]

    @property
    def weeknumStr(self):
        '''今年第几周'''
        return str(self.weeknum)

    @property
    def weekday(self):
        '''星期几'''
        return self.DateTime.isocalendar()[2]

    @property
    def monday(self):
        '''星期一'''
        dt = Date.dateTimeDelta(self.DateTime, "day", -self.weekday + 1)
        return Date(dt)

    @property
    def sunday(self):
        '''星期日'''
        return self.monday.addDay(6)

    @property
    def firstDay(self):
        '''月初'''
        dt = Date.dateTimeDelta(self.DateTime, "day", -self.day + 1)
        return Date(dt)

    @property
    def finalDay(self):
        '''月末'''
        return self.firstDay.addMonth(1).firstDay.addDay(-1)

    @property
    def start(self):
        '''年初'''
        dt = Date("%s0101" % self.year)
        return dt

    @property
    def end(self):
        '''年尾'''
        dt = Date("%s1231" % self.year)
        return dt
    
    @staticmethod
    def dateTimeDelta(datetime, deltatype="day", delta=0):
        '''日期底层操作'''
        if deltatype == "day":
            return datetime + HT.DateTime.timedelta(days=delta)
        elif deltatype == "month":
            if delta > 0:
                while delta > 0:
                    datetime = Date.dateTimeDelta(datetime, 'day', HT.Calendar.monthrange(datetime.year, datetime.month)[1])
                    delta -= 1
                return datetime
            else:
                while delta < 0:
                    y = datetime.year
                    m = datetime.month
                    m -= 1
                    if m <= 0:
                        m = 12
                        y -= 1
                    datetime = Date.dateTimeDelta(datetime, 'day', -HT.Calendar.monthrange(y, m)[1])
                    delta += 1
                return datetime
        elif deltatype == "week":
            return datetime + HT.DateTime.timedelta(days=delta * 7)
        elif deltatype == "year":
            try:
                return datetime.replace(year = datetime.year + delta)
            except ValueError:
                return datetime + (HT.DateTime.date(datetime.year + delta, 3, 1) - HT.DateTime.date(datetime.year, 3, 1))

    def __add__(self, other):
        return self.addDay(int(other))

    def __sub__(self, other):
        return (self.DateTime - other.DateTime).days
    
    def __str__(self):
        return self.string
