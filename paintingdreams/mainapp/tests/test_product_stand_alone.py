from django.test import TestCase
from django.core.exceptions import ValidationError
from mainapp.models import ProductType, Product

class ProductTypeFinalAttributesTestCase(TestCase):
    def setUp(self):
        self.product_type_1 = ProductType.objects.create(
            slug="producttype1",
            title="Product Type 1",
            stand_alone=False)


    def test_product_add_stand_alone_product_type(self):
        """When creating a product without an image it should only be possible to add
        stand alone product types"""
        with self.assertRaises(ValidationError):
            product = Product(product_type=self.product_type_1)
            product.full_clean()
