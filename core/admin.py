from django.contrib import admin

from .models import (
    Customer, Material, Order, OrderItem, Product, Production,
    ProductionMaterial, ProductionProduct, Specification,
    SpecificationItem, UserProfile,
)


admin.site.site_header = "Охрана труда"
admin.site.site_title = "Охрана труда"
admin.site.index_title = "Администрирование системы охраны труда"

admin.site.register([
    Customer, Product, Material, Specification, SpecificationItem,
    Order, OrderItem, Production, ProductionProduct,
    ProductionMaterial, UserProfile,
])
