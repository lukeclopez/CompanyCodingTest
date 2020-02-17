from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Worker(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    year_number = Column(Integer)
    week_number = Column(Integer)
    day_number = Column(Integer)
    hours = Column(Float)


class UtilReport(Base):
    __tablename__ = 'util_reports'

    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    week_number = Column(Integer)
    percent = Column(Float)
