from django.urls import path
from .import views

urlpatterns = [
    path("",views.Index,name="Index"),
    path("MerchantIndex",views.MerchantIndex,name="MerchantIndex"),
    path('SignIn/',views.SignIn,name="SignIn"),
    path("SignUp/",views.SignUp,name="SignUp"),
    path("SignOut/",views.SignOut,name="SignOut"),
    path("FoodMenu",views.FoodMenu,name="FoodMenu"),
    path("my_booking",views.my_booking,name="my_booking"),
    path("add_item_to_order/<int:product_id>",views.add_item_to_order,name="add_item_to_order"),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path("place_order/<int:order_id>/", views.place_order, name="place_order"),
    path("order_summary/<int:order_id>/", views.order_summary, name="order_summary"),
    path("order_summary_all",views.order_summary_all,name="order_summary_all"),
    path("cancel_order/<int:pk>",views.cancel_order,name="cancel_order"),
    path("payment_screen/<int:pk>",views.payment_screen,name="payment_screen"),
    path('payment/success/', views.payment_success, name='payment_success'),

    path("payment_failed",views.payment_failed,name="payment_failed"),
    path("add_rating/<int:pk>",views.add_rating,name="add_rating"),

   

#staff
    path("Menu",views.Menu,name="Menu"),
    path("update_menu_item/<int:pk>",views.update_menu_item, name="update_menu_item"),
    path("delete_menu_item/<int:pk>",views.delete_menu_item,name="delete_menu_item"),
    path("Change_offer_status/<int:pk>",views.Change_offer_status,name="Change_offer_status"),
    path("pending_orders",views.pending_orders,name="pending_orders"),
    path("completed_orders",views.completed_orders,name="completed_orders"),
    path("estimatedtimeadd<int:pk>", views.estimatedtimeadd,name="estimatedtimeadd"),
    path("order_status_change/<int:pk>/<str:status>",views.order_status_change,name="order_status_change")
    

]