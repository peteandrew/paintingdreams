from mainapp.models import Image, Tag, ProductType, Product, ImageWebimage, ProductWebimage
import csv


def clear_data():
    Tag.objects.all().delete()
    Image.objects.all().delete()
    ProductType.objects.all().delete()
    Product.objects.all().delete()


def add_tags():
    with open('populate_data/db_csv/galleries.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            Tag.objects.create(
                slug=row[0],
                name=row[1]
            )


def add_images():
    with open('populate_data/db_csv/images.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            image = Image.objects.create(
                slug=row[0],
                title=row[1],
                description=row[2]
            )
            
            try:
                ImageWebimage.objects.create(
                    image=image,
                    webimage='images/original/' + row[0] + '.jpg'
                )
            except FileNotFoundError:
                pass


def add_image_tags():
    with open('populate_data/db_csv/images_galleries.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            try:
                tag = Tag.objects.get(slug=row[0])
                image = Image.objects.get(slug=row[1])
                image.tags.add(tag)
            except Exception as e:
                print(e)
                print(row)


def add_product_types():
    with open('populate_data/db_csv/products.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0]:
                try:
                    parent = ProductType.objects.get(slug=row[0])
                except:
                    print(row)
                    print("Parent product type not found")
                    continue
            else:
                parent = None
            
            try:            
                ProductType.objects.create(
                    slug=row[1],
                    parent=parent,
                    title=row[2],
                    displayname=row[3],
                    description=row[4],
                    stand_alone=(row[5]=='1'),
                    price=row[6],
                    shipping_weight=row[7],
                    inherit_stand_alone=(row[8]=='1')
                )
            except:
                print(row)


def add_products():
    with open('populate_data/db_csv/image_products.csv') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row[0]) > 0:
                image = Image.objects.get(slug=row[0])
            else:
                image = None
            product_type = ProductType.objects.get(slug=row[1])
            product = Product.objects.create(
                image=image,
                product_type=product_type,
                sold_out=(row[2]=='1'),
                more_due=(row[3]=='1'),
                due_text=row[4]
            )
            
            if image:
                slug = image.slug
            else:
                slug = product_type.slug
            
            try:
                ProductWebimage.objects.create(
                    product=product,
                    webimage='images/original/' + slug + '.jpg'
                )
            except FileNotFoundError:
                pass



clear_data()
add_tags()
add_images()
add_image_tags()
add_product_types()
add_products()
