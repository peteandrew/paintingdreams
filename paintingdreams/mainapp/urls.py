from django.conf.urls import url, include

from mainapp import views

urlpatterns = [
    url(r'^gallery/(.+)$', views.gallery, name='image_index'),
    url(r'^image/(.+)$', views.image_detail, name='image_detail'),
    url(r'^products/(.+)$', views.product_index, name='product_index'),
    url(r'^special-offers$', views.product_special_offer_index, name='product_special-offers'),
    url(r'^new-products$', views.new_product_index, name='new_product_index'),
    url(r'^product/(.+)$', views.product_detail, name='product_detail'),
    url(r'^search$', views.search),
    url(r'^basket-add$', views.basket_add),
    url(r'^basket-change-quantity$', views.basket_change_quantity),
    url(r'^basket-change-destination$', views.basket_change_destination),
    url(r'^basket$', views.basket_show),
    url(r'^apply-discount$', views.apply_discount_code),
    url(r'^order-start$', views.order_start),
    url(r'^order-payment$', views.order_payment),
    url(r'^order-complete$', views.order_transaction_complete, name='order-transaction-complete'),
    url(r'^orders-list$', views.orders_list),
    url(r'^paypal-cancel$', views.paypal_cancel, name='paypal-cancel'),
    url(r'^paypal-ipn', include('paypal.standard.ipn.urls')),
    url(r'^cardsave-result', include('cardsave.urls')),
    url(r'^artist-info$', views.artist_info),
    url(r'^shows$', views.shows),
    url(r'^feedback-old$', views.feedback_old),
    url(r'^feedback$', views.feedback),
    url(r'^wholesale-info$', views.wholesale_info),
    url(r'^cookies$', views.cookies),
    url(r'^delivery-info$', views.delivery_info),
    url(r'^terms-and-conditions$', views.terms_and_conditions),
    url(r'^mailinglist$', views.mailinglist_subscribe),
    url(r'^original_image/(.+)$', views.original_file_serve),
    url(r'^product-stock-counts', views.product_stock_count_list),
    url(r'^festival/(.+)$', views.festival_page, name='festival_page'),

    url(r'^api/images/$', views.ImageListView.as_view()),
    url(r'^api/orders/$', views.OrderListView.as_view()),
    url(r'^api/orders/(.+)/transactions$', views.OrderTransactionListView.as_view()),
    # url(r'^api/orders/(.+)$', views.OrderView.as_view()),
    url(r'^api/search$', views.api_search),

    url(r'^$', views.home)
]
