from wholesale.models import Category, Product, Special, SpecialProductRemoved
import csv


def clear_data():
    Category.objects.all().delete()
    Product.objects.all().delete()
    Special.objects.all().delete()
    SpecialProductRemoved.objects.all().delete()


def add_categories():
    with open('populate_data/db_csv/wholesale_categories.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            Category.objects.create(
                title=row[0]
            )


def add_products():
    with open('populate_data/db_csv/wholesale_products.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                category = Category.objects.get(title=row[3])
            except:
                print(row)
                print("Category not found")
                continue
            
            Product.objects.create(
                code=row[0],
                title=row[1],
                price=row[2],
                category=category,
                new=(row[4]=='1'),
                sold_out=(row[5]=='1')
            )


def add_specials():
    with open('populate_data/db_csv/wholesale_specials.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            Special.objects.create(
                name=row[0],
                postage_option=row[1]
            )


def add_specials_products_removed():
    with open('populate_data/db_csv/wholesale_specials_products_removed.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                special = Special.objects.get(name=row[0])
            except:
                print(row)
                print("Special not found")
                continue
            
            try:
                product = Product.objects.get(code=row[1])
            except:
                print(row)
                print("Product not found")
                continue
            
            SpecialProductRemoved.objects.create(
                special=special,
                product=product
            )


clear_data()
add_categories()
add_products()
add_specials()
add_specials_products_removed()
