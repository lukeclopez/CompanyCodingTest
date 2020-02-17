import argparse
import pathlib
import sys

import constants as c
import database
import utils


def get_input_file_path_from_args():
    my_parser = argparse.ArgumentParser(
        description="Calculate and display worker utilization over several weeks."
    )

    my_parser.add_argument(
        "Path",
        metavar="path",
        type=str,
        help="the path to the input file"
    )

    args = my_parser.parse_args()

    input_file_path = pathlib.Path(args.Path)

    return input_file_path


def sort_all_util_reports(session, weeks: list):
    """
    Since the final output will be sorted by week,
    the first `for` loop iterates over the
    week numbers.

    We store our weekly utilization reports in
    a list of pairs (tuples) because this makes it easy
    to sort with Python's `list.sort()` method.

    List comprehensions could reduce the line count,
    but ultimately they would make the code harder
    to follow in this function.
    """
    names = database.get_all_workers_names(session)

    sorted_util_reports = []
    for w in weeks:
        unsorted_week_of_util_reports = []
        for n in names:
            percent = database.get_percent_util_on_week(session, n, w)
            pair = (n, percent)
            unsorted_week_of_util_reports.append(pair)

        sorted_week_of_util_reports = (
            utils.apply_sorting_rules(unsorted_week_of_util_reports)
        )

        sorted_util_reports.append(sorted_week_of_util_reports)

    return sorted_util_reports


def print_all_util_reports(weeks: list, all_util_reports: list):
    """
    Takes a list of week numbers and
    a list of all utilization reports.

    I print the worker entries with
    four spaces of indentation to
    increase output readability.
    I print a new line after each
    week for the same reason.
    """
    for week_number, util_report in zip(weeks, all_util_reports):
        print(f"Week {week_number}")

        for ur in util_report:
            name = ur[0]
            percent = ur[1]
            print(c.FOUR_SPACES + name, f"{percent}%")

        print("")


if __name__ == "__main__":
    input_path = get_input_file_path_from_args()

    if not input_path.is_file():
        print("The given filename could not be found!")
        sys.exit()

    SessionMaker = database.setup(c.DB_PATH, c.DB_URI)
    session = SessionMaker()
    entries_list = utils.get_entries_from_input_file(input_path)

    database.populate_from_entries(session, entries_list)
    database.create_all_workers_util_reports(session)

    weeks = database.get_unique_weeks(session)

    all_util_reports = sort_all_util_reports(session, weeks)
    print_all_util_reports(weeks, all_util_reports)
