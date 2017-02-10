class MonitorFrequency(object):
    FIVE_MINUTES = 1
    ONE_HOUR = 2
    HALF_DAY = 3


MONITOR_FREQUENCY_CHOICES = (
    (MonitorFrequency.FIVE_MINUTES, '每5分钟'),
    (MonitorFrequency.ONE_HOUR, '每1小时'),
    (MonitorFrequency.HALF_DAY, '每12小时'),
)


class MonitorType(object):
    Contains = 1
    NotContains = 2
    Ping = 3
    GreaterThan = 4
    LessThan = 5
    EqualTo = 6


MONITOR_TYPE_CHOICES = (
    (MonitorType.Contains, '包含'),
    (MonitorType.NotContains, '不包含'),
    (MonitorType.Ping, 'Ping'),
    (MonitorType.GreaterThan, '大于'),
    (MonitorType.LessThan, '小于'),
    (MonitorType.EqualTo, '等于'),
)
