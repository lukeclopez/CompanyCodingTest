from pathlib import Path
import pytest
import sys
import os

from models import Base, Worker, Entry, UtilReport
import program
import database
import utils


def test_parse_entry():
    entry = 'WORKER Vivi "2019-12-25T12:00:00Z/2019-12-25T15:00:00Z"'
    (
        name,
        year_number,
        week_number,
        day_number,
        hours
    ) = database.parse_entry(entry)

    assert (
        name == "Vivi" and
        year_number == 2019 and
        week_number == 52 and
        day_number == 359 and
        hours == 3
    )


def test_database_is_empty(session):
    result = session.query(Worker).all()

    assert result == []


def test_populate_from_entries_adds_all_entries_to_db(entries, session):
    database.populate_from_entries(session, entries)

    entries_in_db = session.query(Entry).all()

    assert len(entries_in_db) == len(entries)


def test_create_all_workers_util_reports(entries, session):
    database.populate_from_entries(session, entries)

    database.create_all_workers_util_reports(session)

    util_reports_count = session.query(UtilReport).count()

    assert util_reports_count
