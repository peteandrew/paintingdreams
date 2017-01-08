from django.test import TestCase
from mainapp.models import ProductType

class ProductTypeFinalAttributesTestCase(TestCase):
    def setUp(self):
        self.product_type_1 = ProductType.objects.create(
            slug="producttype1",
            title="Product Type 1",
            displayname="Test",
            description="Test description",
            stand_alone=True,
            shipping_weight=100)

        self.product_type_2 = ProductType.objects.create(
            slug="producttype2",
            title="Product Type 2",
            inherit_displayname=True,
            inherit_description=True,
            inherit_stand_alone=True,
            inherit_shipping_weight=True,
            parent=self.product_type_1)

        self.product_type_3 = ProductType.objects.create(
            slug="producttype3",
            title="Product Type 3",
            parent=self.product_type_1)

        self.product_type_4 = ProductType.objects.create(
            slug="producttype4",
            title="Product Type 4",
            parent=self.product_type_2)


    def test_get_final_displayname(self):
        """If displayname is set and inherit_displayname is not set then displayname should
        be returned"""
        self.assertEqual(self.product_type_1.displayname_final, "Test")

        """If inherit_displayname and parent are set then the parent's final displayname
        should be returned"""
        self.assertEqual(self.product_type_2.displayname_final, "Test")

        """If displayname and inherit_displayname are not set then title should be returned"""
        self.assertEqual(self.product_type_3.displayname_final, "Product Type 3")


    def test_get_final_description(self):
        """If description is set and inherit_description is not set then description should
        be returned"""
        self.assertEqual(self.product_type_1.description_final, "Test description")

        """If inherit_description and parent are set then the parent's final description
        should be returned"""
        self.assertEqual(self.product_type_2.description_final, "Test description")


    def test_get_final_stand_alone(self):
        """If stand_alone is set and inherit_stand_alone is not set then stand_alone should
        be returned"""
        self.assertEqual(self.product_type_1.stand_alone_final, True)

        """If inherit_stand_alone and parent are set then the parent's final stand_alone
        should be returned"""
        self.assertEqual(self.product_type_2.stand_alone_final, True)


    def test_get_final_shipping_weight(self):
        """If shipping_weight is set and inherit_shipping_weight is not set then shipping_weight should
        be returned"""
        self.assertEqual(self.product_type_1.shipping_weight_final, 100)

        """If inherit_shipping_weight and parent are set then parent's final shipping_weight
        should be returned"""
        self.assertEqual(self.product_type_4.shipping_weight_final, 100)
