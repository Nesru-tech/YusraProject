from django.test import TestCase
from .models import TourPackage

class TourPackageModelTest(TestCase):
    def test_string_representation(self):
        pkg = TourPackage(name="Test Package")
        self.assertEqual(str(pkg), "Test Package")
