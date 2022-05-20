import unittest
from glob import glob
from paper import check_image


class TestPaper(unittest.TestCase):
    # Testing against images on gitrepo.local


    def test_checkWhite(self):
        """
        The above function checks if the image is white or not.
        """
        self.files = ['/home/pi/Pictures/f1630c0c9d7147936613af1e30ae3fa5.jpg', '/home/pi/Pictures/truck.jpg']
        self.IsWhite = ['/home/pi/Pictures/f1630c0c9d7147936613af1e30ae3fa5.jpg']
        self.NotWhite = ['/home/pi/Pictures/truck.jpg']
        for file in self.files:
            check = check_image(file)
            if check:
                self.assertEqual(file in self.IsWhite, True)
            if not check:
                self.assertEqual(file in self.NotWhite, True)

if __name__ == '__main__':
    unittest.main()