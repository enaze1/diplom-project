from django import forms

from .models import (
    Customer,
    Material,
    Order,
    OrderItem,
    Product,
    Production,
    ProductionMaterial,
    ProductionProduct,
    Specification,
    SpecificationItem,
)


class DateInput(forms.DateInput):
    input_type = "date"


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = "__all__"


class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = "__all__"


class SpecificationItemForm(forms.ModelForm):
    class Meta:
        model = SpecificationItem
        fields = ["material", "quantity"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        widgets = {"date": DateInput()}


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "unit_price"]


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = "__all__"
        widgets = {"date": DateInput()}


class ProductionProductForm(forms.ModelForm):
    class Meta:
        model = ProductionProduct
        fields = ["product", "quantity"]


class ProductionMaterialForm(forms.ModelForm):
    class Meta:
        model = ProductionMaterial
        fields = ["material", "quantity"]
