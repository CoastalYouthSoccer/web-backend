from datetime import date
from unittest import TestCase
import pytest
from app.models import (Team, Season, Coach, Association, Address,
                        Venue, SubVenue, Referee, Division)

TEST_ADDRESS = "123 Evergreen Terrace"


@pytest.mark.usefixtures("init_database")
class TestSSeasonTable(TestCase):
    """Test Season Table"""
    def test_season_all(self):
        """Test Query gets correct number of rows"""
        result = self.DB.session.query(Season).all()
        self.assertEqual(len(result), 9, "Not equal to NINE sports rows")

    def test_season_active_true(self):
        """Test to check active, true"""
        result = self.DB.session.query(Season).filter_by(name="Soccer").first()
        print(result)
        self.assertEqual(result.active, True)

    def test_season_active_false(self):
        """Test to check active, false"""
        result = self.DB.session.query(Season).filter_by(name="Baseball").first()
        self.assertEqual(result.active, True)
