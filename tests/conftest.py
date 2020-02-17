"""
This file sets up some things that
I want to use in all my test files.
This saves a lot of duplication, 
especially since I had to 
hack `sys.path`.
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path
import pytest
import sys
import os

# Add some directories to sys.path
# so we can import stuff successfully
# when running from `tests` or
# `CompanyCodingTest`.
current_dir = str(Path.cwd())  # NOQA: E402 (Tell autopep8 not to correct these lines)
parent_dir = str(Path.cwd().parent)  # NOQA: E402
sys.path.append(current_dir)  # NOQA: E402
sys.path.append(parent_dir)  # NOQA: E402

from models import Base, Worker, Entry, UtilReport
import program
import database
import utils


@pytest.fixture
def input_path():
    yield Path("tests/test_input.txt")


@pytest.fixture
def time_entry():
    time_entry = "2019-10-10T13:00:00Z/2019-10-10T23:00:00Z"
    return time_entry.split("/")


@pytest.fixture
def entries(input_path):
    yield utils.get_entries_from_input_file(input_path)


@pytest.fixture
def session():
    DB_PATH = Path("tests/test_db.sqlite")
    DB_URI = f"sqlite:///{DB_PATH}"
    SessionMaker = database.setup(DB_PATH, DB_URI)
    session = SessionMaker()

    yield session

    # Everything after `yield` is the teardown code.
    session.close()


@pytest.fixture
def populated_database(session, entries):
    database.populate_from_entries(session, entries)
    database.create_all_workers_util_reports(session)
