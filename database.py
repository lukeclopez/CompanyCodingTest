from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func
import os

from models import Base, Worker, Entry, UtilReport
import constants as c
import utils


def setup(db_path, db_uri):
    """
    Start with a new db each time so
    we don't need to worry about duplicate entries.
    This method is simpler than wiping only the
    `Entry` table or checking for duplicate `Entry`
    objects.
    """
    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(db_uri)
    Base.metadata.create_all(engine)
    SessionMaker = sessionmaker(bind=engine)

    return SessionMaker


def get_or_create(session: sessionmaker, model: object, **kwargs):
    """
    Takes a database `Session`,
    some kind of model (i.e. `Worker`),
    and any information we would store
    about the given model instance.
    """
    instance = session.query(model).filter_by(**kwargs).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()

    return instance


def parse_entry(entry: str):
    """
    Takes one line of the input file,
    returns all the information contained
    in that line in a tuple.
    """
    entry_parts = entry.split()
    name = entry_parts[1]
    time_entry = entry_parts[2]
    time_entry = time_entry.replace("\"", "").split("/")

    year_number = utils.get_year_number(time_entry)
    week_number = utils.get_week_number(time_entry)
    day_number = utils.get_day_number(time_entry)
    hours = utils.calc_hours(time_entry)

    return name, year_number, week_number, day_number, hours


def populate_from_entries(session: sessionmaker, entries: list):
    """
    This function doesn't return 
    the entries it puts in the database
    because that should be handled
    by a separate function.
    """

    for e in entries:
        name, year_number, week_number, day_number, hours = parse_entry(e)

        worker = get_or_create(session, Worker, name=name)
        session.add(worker)

        entry = Entry(
            worker_id=worker.id,
            year_number=year_number,
            week_number=week_number,
            day_number=day_number,
            hours=hours
        )
        session.add(entry)

    session.commit()


def create_worker_util_reports(session: sessionmaker, worker_id: int, week_hours: dict):
    for week, hours in week_hours.items():
        result = utils.calc_util_percent(hours)
        util_report = UtilReport(
            worker_id=worker_id,
            week_number=week,
            percent=result
        )
        session.add(util_report)


def create_all_workers_util_reports(session: sessionmaker):
    all_workers = session.query(Worker)

    for w in all_workers:
        # How many different days do we have on
        # record for this worker?
        # Also, grab the year number so we can
        # calculate the week number accurately.
        unique_days = (
            session.query(Entry.day_number, Entry.year_number)
            .filter(Entry.worker_id == w.id)
            .distinct()
        )

        # We start on the day level to ensure
        # that anything over 8 hours in one day
        # counts as double hours.
        week_hours = {}
        for ud in unique_days:
            day_hours = (
                session.query(func.sum(Entry.hours))
                .filter(Entry.worker_id == w.id)
                .filter(Entry.day_number == ud.day_number)
                .one()
            )
            day_hours = day_hours[0]

            week_number = utils.get_week_number_from_day_number(
                ud.year_number, ud.day_number)
            # Excess and normal hours are
            # rolled into total hours for
            # the week here.
            weighted_day_hours = utils.get_weighted_day_hours(day_hours)

            week_hours[week_number] = weighted_day_hours

        create_worker_util_reports(session, w.id, week_hours)

    session.commit()


def get_worker_id_from_name(session: sessionmaker, name):
    worker = session.query(Worker).filter(Worker.name == name).first()
    return worker.id


def get_percent_util_on_week(session: sessionmaker, worker_name: str, week_number: int):
    worker_id = get_worker_id_from_name(session, worker_name)

    ut_report = (
        session.query(UtilReport)
        .filter(UtilReport.week_number == week_number)
        .filter(UtilReport.worker_id == worker_id)
        .first()
    )

    final_result = ut_report.percent if ut_report else 0

    return final_result


def get_all_workers_names(session: sessionmaker):
    return [i[0] for i in session.query(Worker.name)]


def get_unique_weeks(session: sessionmaker):
    weeks = session.query(Entry.week_number).distinct()
    return [i[0] for i in weeks]
