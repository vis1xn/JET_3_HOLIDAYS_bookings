import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Time,
)
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = os.getenv(
    "BOOKING_DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/booking_db",
)

Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

class FlightBookingDB(Base):
    __tablename__ = "flight_bookings"

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    flight_number = Column(String(50), nullable=False)
    departure_airport = Column(String(100), nullable=False)
    arrival_airport = Column(String(100), nullable=False)
    departure_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time, nullable=False)


def init_db() -> None:
    """
    Create all tables in the database.
    Safe to call multiple times.
    """
    Base.metadata.create_all(bind=engine)
