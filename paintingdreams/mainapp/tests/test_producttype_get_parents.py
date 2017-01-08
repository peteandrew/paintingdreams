from django.test import TestCase
from mainapp.models import ProductType

class ProductTypeParentsTestCase(TestCase):
    def setUp(self):
        product_type_1 = ProductType.objects.create(
            slug="producttype1",
            title="Product Type 1")

        product_type_2 = ProductType.objects.create(
            slug="producttype2",
            title="Product Type 2",
            parent=product_type_1)

        self.product_type_3 = ProductType.objects.create(
            slug="producttype3",
            title="Product Type 3",
            parent=product_type_2)


    def test_get_producttype_parents(self):
        product_type_3_parents = self.product_type_3.parents()
        self.assertEqual(len(product_type_3_parents), 2)
        

