from django.urls import path
from .views import login_view, logout_view, index_view, customer_delete_view, customer_edit_view, customer_add_view


urlpatterns = [
    path("", index_view, name='index-url'),
    path('add/', customer_add_view, name='customer-add-url'),
    path('login', login_view, name='login-url'),
    path('logout', logout_view, name='logout-url'),
    path("<int:customer_id>/delete", customer_delete_view, name='customer-delete-url'),
    path("<int:customer_id>/edit", customer_edit_view, name='customer-edit-url'),
]