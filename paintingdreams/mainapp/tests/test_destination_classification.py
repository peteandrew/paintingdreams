from django.test import TestCase

from mainapp import destination_classification


class DestinationClassificationTestCase(TestCase):

    def test_classify_gb_destination(self):
        self.assertEqual(destination_classification.classify('GB'), 'GB')


    def test_classify_europe_destination(self):
        self.assertEqual(destination_classification.classify('FR'), 'EUROPE')
        self.assertEqual(destination_classification.classify('ES'), 'EUROPE')
        self.assertEqual(destination_classification.classify('DE'), 'EUROPE')


    def test_classify_worldwide_destination(self):
        self.assertEqual(destination_classification.classify('AU'), 'WORLD')
        self.assertEqual(destination_classification.classify('JP'), 'WORLD')


    def test_classify_us_destination(self):
        self.assertEqual(destination_classification.classify('US'), 'US')