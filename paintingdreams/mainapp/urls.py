from django.conf.urls import patterns, url, include

from mainapp import views

urlpatterns = patterns('',
    url(r'^images/$', views.image_index, name='image_index'),
    url(r'^images/tag/(.+)$', views.image_tag_index, name='image_tag_index'),
    url(r'^images/(.+)$', views.image_detail, name='image_detail'),
    url(r'^products/$', views.product_index, name='product_index'),
    url(r'^products/type/(.+)$', views.product_index, name='product_type_index'),
    url(r'^products/(.+)$', views.product_detail, name='product_detail'),
    url(r'^search$', views.search),
    url(r'^basket-add$', views.basket_add),
    url(r'^basket-change-quantity$', views.basket_change_quantity),
    url(r'^basket-change-destination$', views.basket_change_destination),
    url(r'^basket$', views.basket_show),
    url(r'^order-start$', views.order_start),
    url(r'^order-payment$', views.order_payment),
    url(r'^order-complete$', views.order_transaction_complete, name='order-transaction-complete'),
    url(r'^paypal-cancel$', views.paypal_cancel, name='paypal-cancel'),
    (r'^paypal-ipn$', include('paypal.standard.ipn.urls')),
    (r'^cardsave-result', include('cardsave.urls')),
    url(r'^artist-info$', views.artist_info),
    url(r'^shows$', views.shows),
    url(r'^feedback$', views.feedback),
    url(r'^wholesale-info$', views.wholesale_info),
    url(r'^delivery-info$', views.delivery_info),
    url(r'^terms-and-conditions$', views.terms_and_conditions),
    url(r'^mail-test$', views.mailtest),
    url(r'^original_image/(.+)$', views.original_file_serve),

    url(r'^session-order$', views.session_order),
    url(r'^complete-order-transaction$', views.temp_complete_order_transaction),

    url(r'^api/images/$', views.ImageListView.as_view()),
    url(r'^api/orders/$', views.OrderListView.as_view()),
    url(r'^api/orders/(.+)/transactions$', views.OrderTransactionListView.as_view()),
    # url(r'^api/orders/(.+)$', views.OrderView.as_view()),
    url(r'^api/search$', views.api_search),

    url(r'^$', views.home)
)
