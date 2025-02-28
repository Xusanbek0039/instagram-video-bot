import unittest
from unittest.mock import patch, MagicMock
import os
from main import check_user_limit, download_instagram_video

class TestInstagramBot(unittest.TestCase):
    
    def setUp(self):
        # Test uchun vaqtincha fayllar yaratamiz
        self.test_user_limits = "test_user_limits.txt"
        self.test_counter = "test_counter.txt"
        
        with open(self.test_user_limits, "w") as f:
            f.write("12345 2\n")  # Telegram user_id bilan foydalanish limiti
        
        with open(self.test_counter, "w") as f:
            f.write("5")  # Umumiy yuklab olingan videolar soni
    
    def tearDown(self):
        # Testdan keyin vaqtincha fayllarni o‘chiramiz
        if os.path.exists(self.test_user_limits):
            os.remove(self.test_user_limits)
        if os.path.exists(self.test_counter):
            os.remove(self.test_counter)
    
    def test_check_user_limit(self):
        self.assertTrue(check_user_limit("12345", self.test_user_limits))
        self.assertFalse(check_user_limit("67890", self.test_user_limits))
    

    
    @patch("requests.get")
    def test_download_instagram_video(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Fake Video Content"
        mock_get.return_value = mock_response
        
        url = "https://www.instagram.com/reel/abc123/"
        filename = download_instagram_video(url)
        
        self.assertIsNotNone(filename)
        self.assertTrue(os.path.exists(filename))
        
        os.remove(filename)  # Testdan keyin faylni o‘chiramiz

if __name__ == "__main__":
    unittest.main()