from datetime import timedelta, datetime
import iso8601

import constants as c


def get_entries_from_input_file(input_path):
    """
    Since each entry is on a
    separate line, split on line breaks.
    """
    with open(input_path) as input_file:
        entries_list = input_file.read().strip().split("\n")

    return entries_list


def parse_times(time_entry: str):
    times = [iso8601.parse_date(i) for i in time_entry]
    start_time = times[0]
    end_time = times[1]

    return start_time, end_time


def calc_hours(time_entry: str):
    start_time, end_time = parse_times(time_entry)

    delta = end_time - start_time
    hours = delta.total_seconds() / c.SECONDS_IN_HOUR

    return hours


def get_year_number(time_entry: str):
    start_time, end_time = parse_times(time_entry)
    year_number = end_time.isocalendar()[0]

    return year_number


def get_week_number(time_entry: str):
    start_time, end_time = parse_times(time_entry)
    week_number = end_time.isocalendar()[1]

    return week_number


def get_day_number(time_entry: str):
    start_time, end_time = parse_times(time_entry)
    day_number = end_time.timetuple().tm_yday

    return day_number


def get_week_number_from_day_number(current_year: int, day_number: int):
    """
    Takes the year and day number.
    We need the year to ensure
    precision, since the first
    day of the year can be a Wednesday
    on one year and a Sunday on another
    year.
    """
    day_of_year = "%j"
    date = datetime.strptime(str(day_number), day_of_year)
    date = date.replace(year=current_year)

    return date.isocalendar()[1]


def get_weighted_day_hours(day_hours: int):
    if day_hours > c.HOURS_IN_WORK_DAY:
        weighted_day_hours = (
            day_hours +
            (day_hours - c.HOURS_IN_WORK_DAY)
        )
    else:
        weighted_day_hours = day_hours

    return weighted_day_hours


def calc_util_percent(week_hours: int):
    return (week_hours / c.HOURS_IN_WORK_WEEK) * 100


def get_percent(x):
    """
    Since our utilization report
    list is a list of pairs and
    the second item is the percent,
    we sort by the second item.
    """
    return x[1]


def put_percents_over_100_at_top(names_percents_pairs):
    # I copied the list because you
    # should never modify something
    # that you're iterating over.
    names_percents_pairs_copy = names_percents_pairs.copy()

    percents_over_100 = []
    for ur in names_percents_pairs:
        name = ur[0]
        percent = ur[1]

        if percent > 100:
            index = names_percents_pairs_copy.index(ur)
            util_over_100 = names_percents_pairs_copy.pop(index)
            percents_over_100.append(util_over_100)

    # I sort the list again here so that even
    # the percents over 100 are in ascending
    # order.
    percents_over_100.sort(key=get_percent)

    return percents_over_100 + names_percents_pairs_copy


def apply_sorting_rules(util_reports_for_week: list):
    util_reports_for_week.sort(key=get_percent)

    util_reports_for_week = put_percents_over_100_at_top(util_reports_for_week)

    return util_reports_for_week
