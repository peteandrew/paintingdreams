from django.test import TestCase
from mainapp.models import ProductType

class ProductTypeChildrenTestCase(TestCase):
    def setUp(self):
        self.product_type_1 = ProductType.objects.create(
            slug="producttype1",
            title="Product Type 1")

        product_type_2 = ProductType.objects.create(
            slug="producttype2",
            title="Product Type 2",
            parent=self.product_type_1)

        product_type_3 = ProductType.objects.create(
            slug="producttype3",
            title="Product Type 3",
            parent=self.product_type_1)

        product_type_4 = ProductType.objects.create(
            slug="producttype4",
            title="Product Type 4",
            parent=product_type_2)


    def test_get_producttype_children(self):
        product_type_1_children = self.product_type_1.children()
        self.assertEqual(len(product_type_1_children), 3)
        
