# CronScheduleTriggers: Quartz Syntax based Cron Trigger library.

[![pipeline status](https://gitlab.com/dameon.andersen/cstriggers/badges/master/pipeline.svg)](https://gitlab.com/dameon.andersen/cstriggers/commits/master) [![coverage report](https://gitlab.com/dameon.andersen/cstriggers/badges/master/coverage.svg)](https://gitlab.com/dameon.andersen/cstriggers/commits/master)

 Cron Schedule Triggers (CSTriggers) is a Python library enabling the ability to determine the next execution of a live schedule. Its syntax is that of [Quartz Job Scheduler](http://www.quartz-scheduler.org). This library is not a scheduling app or a task queue, there are plenty of those in the wild to choose from. When you need advanced customisation of triggers for tasks, and a common and conventional syntax for schedule notation, CSTriggers comes to your aid. 
 
## This library is for those who

 - Want the ability to generate future task data for visualization purposes.
 - Want to combine their own choice of solutions to build a customizable integrated task queuing/scheduling system at any scale.
 - Do not want to run java, but want to take advantage of the rich _Quartz Cron_ syntax
 - Do not want to drag in many dependencies into their project (Uses standard Python3 libraries only).


## Example usage

Initialize a schedule object with a cron notation string, a start date, and an optional end date. Call `.next_trigger()` for a new date. Notice that when an end_date is given, The schedule terminates at `2022-10-13T00:00:00` and not `2030-03-01T00:00:00` as it would naturally.

```python
from cstriggers.core.trigger import QuartzCron

schedule_string = "0 0 0 1 JAN-MAR ? 2010-2030"
start_date = "2019-10-13T00:00:00"
end_date = "2022-10-13T00:00:00"
cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)

print(cron_obj.next_trigger(isoformat=True))
```
```
>> 2020-01-01T00:00:00
```

For multiple sequential dates call either `.next_trigger()` multiple times.

```python
from cstriggers.core.trigger import QuartzCron

schedule_string = "0 0 0 1 JAN-MAR ? 2010-2030"
start_date = "2019-10-13T00:00:00"
end_date = "2022-10-13T00:00:00"
cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)

print(cron_obj.next_trigger(isoformat=True))
print(cron_obj.next_trigger(isoformat=True))

```

```
>> 2020-01-01T00:00:00
>> 2020-02-01T00:00:00
```

Or call `.next_triggers()` with the number of triggers needed. 

```python
from cstriggers.core.trigger import QuartzCron

schedule_string = "0 0 0 1 JAN-MAR ? 2010-2030"
start_date = "2019-10-13T00:00:00"
end_date = "2022-10-13T00:00:00"
cron_obj = QuartzCron(schedule_string=schedule_string, start_date=start_date, end_date=end_date)

print(cron_obj.next_triggers(number_of_triggers=10, isoformat=True))
```

```
>> [
    '2020-01-01T00:00:00', 
    '2020-02-01T00:00:00', 
    '2020-03-01T00:00:00', 
    '2021-01-01T00:00:00', 
    '2021-02-01T00:00:00', 
    '2021-03-01T00:00:00', 
    '2022-01-01T00:00:00', 
    '2022-02-01T00:00:00', 
    '2022-03-01T00:00:00', 
    '2023-01-01T00:00:00'
]
```

## Roadmap
- Support for last_trigger(s) to retroactively look at schedule dates.
- Support for AWS Cron Expression syntax.