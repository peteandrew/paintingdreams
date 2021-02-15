from django.test import TestCase
from mainapp.models import ProductType, ProductTypeDestinationShippingWeightOverride

class ProductTypeFinalAttributesTestCase(TestCase):
    def setUp(self):
        self.product_type_1 = ProductType.objects.create(
            slug="producttype1",
            title="Product Type 1",
            displayname="Test",
            description="Test description",
            stand_alone=True,
            shipping_weight=100,
            shipping_weight_multiple=50,
        )

        self.product_type_2 = ProductType.objects.create(
            slug="producttype2",
            title="Product Type 2",
            inherit_displayname=True,
            inherit_description=True,
            inherit_stand_alone=True,
            inherit_shipping_weight=True,
            inherit_shipping_weight_multiple=True,
            parent=self.product_type_1)

        self.product_type_3 = ProductType.objects.create(
            slug="producttype3",
            title="Product Type 3",
            shipping_weight=150,
            parent=self.product_type_1)

        ProductTypeDestinationShippingWeightOverride.objects.create(
            product_type=self.product_type_1,
            destination='WORLD',
            shipping_weight=500,
            shipping_weight_multiple=300,
        )


    def test_get_final_displayname(self):
        # If displayname is set and inherit_displayname is not set then displayname should
        # be returned
        self.assertEqual(self.product_type_1.displayname_final, "Test")

        # If inherit_displayname and parent are set then the parent's final displayname
        # should be returned
        self.assertEqual(self.product_type_2.displayname_final, "Test")

        # If displayname and inherit_displayname are not set then title should be returned
        self.assertEqual(self.product_type_3.displayname_final, "Product Type 3")


    def test_get_final_description(self):
        # If description is set and inherit_description is not set then description should
        # be returned
        self.assertEqual(self.product_type_1.description_final, "Test description")

        # If inherit_description and parent are set then the parent's final description
        # should be returned
        self.assertEqual(self.product_type_2.description_final, "Test description")


    def test_get_final_stand_alone(self):
        # If stand_alone is set and inherit_stand_alone is not set then stand_alone should
        # be returned
        self.assertEqual(self.product_type_1.stand_alone_final, True)

        # If inherit_stand_alone and parent are set then the parent's final stand_alone
        # should be returned
        self.assertEqual(self.product_type_2.stand_alone_final, True)


    def test_get_final_shipping_weight(self):
        # If shipping_weight is set and inherit_shipping_weight is not set then shipping_weight should
        # be returned
        self.assertEqual(self.product_type_1.shipping_weight_final(), 100)
        self.assertEqual(self.product_type_3.shipping_weight_final(), 150)

        # If inherit_shipping_weight and parent are set then parent's final shipping_weight
        # should be returned
        self.assertEqual(self.product_type_2.shipping_weight_final(), 100)


    def test_get_final_shipping_weight_multiple(self):
        self.assertEqual(self.product_type_1.shipping_weight_multiple_final(), 50)

        # If inherit_shipping_weight_multiple is set then parent's final shipping_weight_multiple
        # should be returned
        self.assertEqual(self.product_type_2.shipping_weight_multiple_final(), 50)

        # If inherit_shipping_weight_multiple is not set and shipping_weight is set then
        # shipping_weight should be returned
        self.assertEqual(self.product_type_3.shipping_weight_multiple_final(), 150)


    def test_get_final_shipping_weight_destination_override(self):
        # If ProductTypeDestinationShippingWeightOverride exists for product type and destination
        # then this shipping_weight and shipping_weight_multiple should be used
        self.assertEqual(self.product_type_1.shipping_weight_final("WORLD"), 500)
        self.assertEqual(self.product_type_2.shipping_weight_final("WORLD"), 500)
        # If inherit_shipping_weight is not set, then shipping_weight_final should be returned
        self.assertEqual(self.product_type_3.shipping_weight_final("WORLD"), 150)

        self.assertEqual(self.product_type_1.shipping_weight_multiple_final("WORLD"), 300)
        self.assertEqual(self.product_type_2.shipping_weight_multiple_final("WORLD"), 300)
        # If inherit_shipping_weight is not set, then shipping_weight_final should be returned
        self.assertEqual(self.product_type_3.shipping_weight_multiple_final("WORLD"), 150)

        # If shipping_weight_multiple on destination override is not set, shipping_weight on
        # destination override should be used instead
        ProductTypeDestinationShippingWeightOverride.objects.all().delete()
        ProductTypeDestinationShippingWeightOverride.objects.create(
            product_type=self.product_type_1,
            destination='WORLD',
            shipping_weight=500,
        )
        self.assertEqual(self.product_type_1.shipping_weight_multiple_final("WORLD"), 500)
