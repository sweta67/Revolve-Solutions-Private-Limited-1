import pytest
from task import *
# pip install -U pytest


def test_total_number_of_days():
    result = total_number_of_days("flights.csv")
    assert result == 365


def test_departure_cities():
    result = departure_cities("flights.csv", "airports.csv")
    assert result == {"New York", "Newark"}


def test_relationship():
    result = relationship("flights.csv", "Planes.csv")
    assert result == ["year", "tailnum"]


def test_manufacturer_with_most_delays():
    result = manufacturer_with_most_delays("flights.csv", "planes.csv")
    assert result == "EMBRAER"


def test_two_most_connected_cities():
    result = two_most_connected_cities("flights.csv", "airports.csv")
    assert result == ["New York", "Los Angeles"]


# This is the output
#  pytest tests.py
# ========================= test session starts =========================
# platform darwin -- Python 3.10.1, pytest-7.0.1, pluggy-1.0.0
# rootdir: /Users/Sweta Chaubey/Desktop/revolve_task
# collected 5 items

# tests.py .....                                                  [100%]

# ========================== 5 passed in 2.67s ==========================