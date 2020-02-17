from datetime import timedelta, datetime
from pathlib import Path
import random
import pytest
import sys
import os

from models import UtilReport
from constants import *
import database
import iso8601
import utils


def test_get_entries_from_input_file_makes_entry_for_each_line(entries, input_path):
    entries = utils.get_entries_from_input_file(input_path)

    with open(input_path) as input_file:
        line_count = len(input_file.readlines())

    assert len(entries) == line_count


def test_parse_times_returns_two_datetime_objects(time_entry):
    start_time, end_time = utils.parse_times(time_entry)

    assert (
        isinstance(start_time, datetime) and
        isinstance(end_time, datetime)
    )


def test_calc_hours_calculates_correctly(time_entry):
    hours = utils.calc_hours(time_entry)

    assert hours == 10


@pytest.mark.parametrize(
    "input_hours, expected_weighted_hours",
    [(0, 0), (1, 1), (8, 8), (9, 10), (10, 12), (16, 24)]
)
def test_get_weighted_day_hours_calculates_correctly(input_hours, expected_weighted_hours):
    hours = utils.get_weighted_day_hours(input_hours)

    assert hours == expected_weighted_hours


def test_put_percents_over_100_at_top():
    over_100 = 105
    percents = [0, 50, 99, over_100]
    unsorted_util_reports = [("name", i) for i in percents]

    sorted_util_reports = utils.put_percents_over_100_at_top(
        unsorted_util_reports
    )

    first_percent_in_list = sorted_util_reports[0][1]

    assert first_percent_in_list == over_100


def test_apply_sorting_rules_does_ascending_order():
    percents = [96, 42, 53, 99]
    unsorted_util_reports = [("name", i) for i in percents]

    percents.sort()
    expected_result = [("name", i) for i in percents]

    sorted_util_reports = utils.apply_sorting_rules(
        unsorted_util_reports
    )

    assert sorted_util_reports == expected_result
