import json
from django.db import connection
from base64 import b64decode
from mainapp.models import Product

cursor = connection.cursor()
cursor.execute("select session_key, session_data, expire_date from django_session where expire_date > '2021-02-01' ORDER BY expire_date")

while True:
    row = cursor.fetchone()
    if row == None:
        break

    decoded_session_data = str(b64decode(row[1]))
    if 'CART' not in decoded_session_data:
        continue
    if 'order_id' in decoded_session_data:
        continue

    data = json.loads(
        decoded_session_data[
            decoded_session_data.find(':') + 1 : -1
        ]
    )
    items = data['CART']
    if len(items) == 0:
        continue

    print(f'Session key: {row[0]}')
    print(f'Expiry date: {row[2]}')

    for item_key in items.keys():
        item = items[item_key]
        product = Product.objects.get(pk=item['product_pk'])
        print(f'{item["quantity"]} x {product} - £{item["price"]}')

    print("")
