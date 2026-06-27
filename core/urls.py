from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("customers/", views.customers, name="customers"),
    path("customers/add/", views.customer_add, name="customer_add"),
    path("products/", views.products, name="products"),
    path("products/add/", views.product_add, name="product_add"),
    path("materials/", views.materials, name="materials"),
    path("materials/add/", views.material_add, name="material_add"),
    path("specifications/", views.specifications, name="specifications"),
    path("specifications/add/", views.specification_add, name="specification_add"),
    path("specifications/<int:pk>/", views.specification_detail, name="specification_detail"),
    path("orders/", views.orders, name="orders"),
    path("orders/add/", views.order_add, name="order_add"),
    path("orders/<int:pk>/", views.order_detail, name="order_detail"),
    path("production/", views.production_list, name="production"),
    path("production/add/", views.production_add, name="production_add"),
    path("production/<int:pk>/", views.production_detail, name="production_detail"),
    path("reports/cost/", views.cost_report, name="cost_report"),
    path("users/", views.users, name="users"),
    path("help/", views.help_page, name="help"),
]
