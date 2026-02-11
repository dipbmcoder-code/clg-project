import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import date, datetime
import json

# Add the parent directory to the sys.path to allow imports from other modules
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from player_abroad.insert_player_abroad_api import (
    insert_player_abroad_api,
    current_db_abroad_players,
    check_data_exists_in_db,
    insert_db_player_abroad,
    check_is_posted,
    update_player_abroad_post_in_db,
    get_current_completed_fixtures
)
from player_abroad.image_player_abroad_api import generate_player_abroad_image
from player_abroad.main_player_abroad import main_player_abroad

class TestPlayerAbroadModule(unittest.TestCase):

    def setUp(self):
        self.mock_player_data = {
            "fixtureId": 1,
            "date": "2024-01-01T12:00:00+00:00",
            "venue": "Test Stadium",
            "city": "Test City",
            "leagueId": 10,
            "league": "Test League",
            "leagueCountry": "Testland",
            "leagueSeason": 2024,
            "homeTeam": "Home Team",
            "awayTeam": "Away Team",
            "score": {"home": 2, "away": 1},
            "playerId": 123,
            "playerName": "Test Player",
            "eventType": "Goal",
            "eventDetail": "Penalty",
            "team": "Home Team",
            "teamId": 1,
            "minutes": "45",
            "goalsCount": 1,
            "playerDetails": {
                "firstname": "Test",
                "lastname": "Player",
                "age": 25,
                "birth": {"date": "1999-01-01", "place": "Test Place", "country": "Testland"},
                "nationality": "Testland",
                "height": "180cm",
                "weight": "75kg",
                "injured": False,
                "photo": "http://example.com/photo.jpg",
                "statistics": []
            }
        }
        self.mock_db_record = {
            "player_id": 123,
            "is_posted": False,
            "fixture_id": 1,
            "event_type": "Goal",
            "event_detail": "Penalty",
            "website_ids": None
        }

    @patch('player_abroad.insert_player_abroad_api.get_completed_fixtures')
    def test_get_current_completed_fixtures(self, mock_get_completed_fixtures):
        """
        Test case to verify retrieval of current completed fixtures.
        """
        try:
            mock_get_completed_fixtures.return_value = [{"fixture": {"id": 1}}]
            result = get_current_completed_fixtures()
            self.assertEqual(result, [{"fixture": {"id": 1}}])
            print("test_get_current_completed_fixtures: PASSED")
        except AssertionError as e:
            print(f"test_get_current_completed_fixtures: FAILED - {e}")
            raise

    @patch('player_abroad.insert_player_abroad_api.scrap_current_date_data')
    @patch('player_abroad.insert_player_abroad_api.get_player_profile_info')
    @patch('player_abroad.insert_player_abroad_api.get_player_info_with_statistics')
    @patch('player_abroad.insert_player_abroad_api.get_fixture_events')
    def test_insert_player_abroad_api(self, mock_get_fixture_events, mock_get_player_info_with_statistics, mock_get_player_profile_info, mock_scrap_current_date_data):
        """
        Test case to verify insertion of player abroad data via API.
        """
        try:
            mock_get_fixture_events.return_value = [
                {
                    "player": {"id": 123, "name": "Test Player"},
                    "type": "Goal",
                    "detail": "Penalty",
                    "time": {"elapsed": 45},
                    "team": {"name": "Home Team", "id": 1}
                }
            ]
            mock_get_player_info_with_statistics.return_value = {
                "player": {"firstname": "Test", "lastname": "Player", "nationality": "Otherland", "birth": {"date": "1999-01-01"}, "name": "Test Player"},
                "statistics": []
            }
            mock_get_player_profile_info.return_value = {"firstname": "Test", "lastname": "Player", "nationality": "Otherland", "birth": {"date": "1999-01-01"}, "name": "Test Player"}
            mock_scrap_current_date_data.return_value = []
            
            fixtures = [
                {
                    "fixture": {"id": 1, "date": "2024-01-01T12:00:00+00:00", "venue": {"name": "Test Stadium", "city": "Test City"}},
                    "league": {"id": 10, "name": "Test League", "country": "Testland", "season": 2024},
                    "teams": {"home": {"name": "Home Team"}, "away": {"name": "Away Team"}},
                    "score": {"fulltime": {"home": 2, "away": 1}}
                }
            ]
            league_ids = [10]
            types = "player_abroad"
            countries = ["Testland"]
            
            result = insert_player_abroad_api(fixtures, league_ids, types, countries)
            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['playerId'], 123)
            print("test_insert_player_abroad_api: PASSED")
        except AssertionError as e:
            print(f"test_insert_abroad_player_api: FAILED - {e}")
            raise

    @patch('player_abroad.insert_player_abroad_api.get_data')
    def test_current_db_abroad_players(self, mock_get_data):
        """
        Test case to verify retrieval of current abroad players from the database.
        """
        try:
            mock_get_data.return_value = [self.mock_db_record]
            result = current_db_abroad_players()
            self.assertEqual(result, [self.mock_db_record])
            print("test_current_db_abroad_players: PASSED")
        except AssertionError as e:
            print(f"test_current_db_abroad_players: FAILED - {e}")
            raise

    def test_check_data_exists_in_db(self):
        """
        Test case to verify checking for existing data in the database.
        """
        try:
            db_player_abroads = [self.mock_db_record]
            result = check_data_exists_in_db(self.mock_player_data, db_player_abroads)
            self.assertTrue(result)
            print("test_check_data_exists_in_db: PASSED")
        except AssertionError as e:
            print(f"test_check_data_exists_in_db: FAILED - {e}")
            raise

    @patch('player_abroad.insert_player_abroad_api.insert_db')
    @patch('player_abroad.insert_player_abroad_api.get_data_one')
    def test_insert_db_player_abroad(self, mock_get_data_one, mock_insert_db):
        """
        Test case to verify insertion of player abroad data into the database.
        """
        try:
            mock_get_data_one.return_value = self.mock_db_record
            result = insert_db_player_abroad(self.mock_player_data)
            self.assertEqual(result, self.mock_db_record)
            mock_insert_db.assert_called_once()
            print("test_insert_db_player_abroad: PASSED")
        except AssertionError as e:
            print(f"test_insert_db_player_abroad: FAILED - {e}")
            raise

    def test_check_is_posted(self):
        """
        Test case to verify checking if a player abroad record is posted.
        """
        try:
            player = {"fixtureId": 1, "playerId": 123, "eventType": "Goal", "eventDetail": "Penalty"}
            db_player_abroads = [{'player_id': 123, 'is_posted': True, 'fixture_id': 1, 'event_type': 'Goal', 'event_detail': 'Penalty', 'website_ids': [1]}]
            website_id = 1
            result = check_is_posted(player, db_player_abroads, website_id)
            self.assertTrue(result)
            print("test_check_is_posted: PASSED")
        except AssertionError as e:
            print(f"test_check_is_posted: FAILED - {e}")
            raise

    @patch('player_abroad.insert_player_abroad_api.insert_db')
    def test_update_player_abroad_post_in_db(self, mock_insert_db):
        """
        Test case to verify updating the post status of a player abroad record.
        """
        try:
            player = {"playerId": 123, "fixtureId": 1, "eventType": "Goal", "eventDetail": "Penalty"}
            website_ids = [1, 2]
            update_player_abroad_post_in_db(player, website_ids)
            mock_insert_db.assert_called_once()
            print("test_update_player_abroad_post_in_db: PASSED")
        except AssertionError as e:
            print(f"test_update_player_abroad_post_in_db: FAILED - {e}")
            raise

    @patch('player_abroad.image_player_abroad_api.generate_openRouter_image')
    def test_generate_player_abroad_image(self, mock_generate_openRouter_image):
        """
        Test case to verify the generation of a player abroad image.
        """
        try:
            player = {"playerId": 123, "playerName": "Test Player", "fixtureId": 1, "eventType": "Goal", "eventDetail": "Penalty", "league": "Test League"}
            l_version = 'eng'
            types = 'player_abroad'
            key = "1_123_Goal_Penalty"
            generate_player_abroad_image(player, l_version, types, key)
            mock_generate_openRouter_image.assert_called_once()
            print("test_generate_player_abroad_image: PASSED")
        except AssertionError as e:
            print(f"test_generate_player_abroad_image: FAILED - {e}")
            raise

    @patch('player_abroad.main_player_abroad.get_websites')
    @patch('player_abroad.main_player_abroad.check_enable_for')
    @patch('player_abroad.main_player_abroad.filter_websites_by_enable')
    @patch('player_abroad.main_player_abroad.get_websites_leagues')
    @patch('player_abroad.main_player_abroad.get_unique_field')
    @patch('player_abroad.main_player_abroad.insert_player_abroad_api')
    @patch('player_abroad.main_player_abroad.current_db_abroad_players')
    @patch('player_abroad.main_player_abroad.check_data_exists_in_db')
    @patch('player_abroad.main_player_abroad.insert_db_player_abroad')
    @patch('player_abroad.main_player_abroad.check_is_posted')
    @patch('player_abroad.main_player_abroad.generate_player_abroad_image')
    @patch('player_abroad.main_player_abroad.save_aws')
    @patch('player_abroad.main_player_abroad.main_publication2')
    @patch('player_abroad.main_player_abroad.delete_img')
    @patch('player_abroad.main_player_abroad.update_player_abroad_post_in_db')
    def test_main_player_abroad_logic(self, mock_update_post, mock_delete_img, mock_main_publication2, mock_save_aws, mock_generate_image, mock_check_is_posted, mock_insert_db_player_abroad, mock_check_data_exists_in_db, mock_current_db_abroad_players, mock_insert_player_abroad_api, mock_get_unique_field, mock_get_websites_leagues, mock_filter_websites_by_enable, mock_check_enable_for, mock_get_websites):
        """
        Test case to verify the main logic of the player abroad module.
        """
        try:
            mock_get_websites.return_value = [{"documentId": 1, "l_version": "eng", "player_abroad_countries": ["Testland"]}]
            mock_check_enable_for.return_value = True
            mock_filter_websites_by_enable.return_value = [{"documentId": 1, "l_version": "eng", "player_abroad_countries": ["Testland"]}]
            mock_get_websites_leagues.return_value = [10]
            mock_get_unique_field.return_value = ["Testland"]
            mock_insert_player_abroad_api.return_value = [self.mock_player_data]
            mock_current_db_abroad_players.return_value = []
            mock_check_data_exists_in_db.return_value = False
            mock_insert_db_player_abroad.return_value = self.mock_db_record
            mock_check_is_posted.return_value = False

            main_player_abroad(test_fixtures=[{"fixture": {"id": 1}}])

            mock_get_websites.assert_called_once()
            mock_check_enable_for.assert_called_once()
            mock_filter_websites_by_enable.assert_called_once()
            mock_get_websites_leagues.assert_called_once()
            mock_get_unique_field.assert_called_once()
            mock_insert_player_abroad_api.assert_called_once()
            mock_current_db_abroad_players.assert_called_once()
            mock_check_data_exists_in_db.assert_called_once()
            mock_insert_db_player_abroad.assert_called_once()
            mock_check_is_posted.assert_called_once()
            mock_generate_image.assert_called_once()
            mock_save_aws.assert_called_once()
            mock_main_publication2.assert_called_once()
            mock_delete_img.assert_called_once()
            mock_update_post.assert_called_once()
            print("test_main_player_abroad_logic: PASSED")
        except AssertionError as e:
            print(f"test_main_player_abroad_logic: FAILED - {e}")
            raise

if __name__ == '__main__':
    unittest.main()