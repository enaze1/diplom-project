from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CustomerForm,
    MaterialForm,
    OrderForm,
    OrderItemForm,
    ProductForm,
    ProductionForm,
    ProductionMaterialForm,
    ProductionProductForm,
    SpecificationForm,
    SpecificationItemForm,
)
from .models import Customer, Material, Order, Product, Production, Specification


def save_form(request, form_class, title, return_url):
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(return_url)
    return render(request, "core/form.html", {"form": form, "title": title})


@login_required
def dashboard(request):
    context = {
        "customer_count": Customer.objects.count(),
        "product_count": Product.objects.count(),
        "material_count": Material.objects.count(),
        "order_count": Order.objects.count(),
        "recent_orders": Order.objects.select_related("customer")[:5],
    }
    return render(request, "core/dashboard.html", context)


@login_required
def customers(request):
    rows = [[item.source_id, item.name, item.inn or "-", item.address or "-", item.phone or "-"] for item in Customer.objects.all()]
    return render(request, "core/table.html", {
        "title": "Сотрудники",
        "headers": ["Таб. номер", "ФИО", "СНИЛС", "Подразделение и должность", "Телефон"],
        "rows": rows,
        "add_url": "customer_add",
    })


@login_required
def customer_add(request):
    return save_form(request, CustomerForm, "Новый сотрудник", "customers")


@login_required
def products(request):
    rows = [[item.code or "-", item.name, item.unit, item.sale_price] for item in Product.objects.all()]
    return render(request, "core/table.html", {
        "title": "Программы обучения",
        "headers": ["Код", "Наименование", "Ед.", "Плановая стоимость"],
        "rows": rows,
        "add_url": "product_add",
    })


@login_required
def product_add(request):
    return save_form(request, ProductForm, "Новая программа обучения", "products")


@login_required
def materials(request):
    rows = [[item.code or "-", item.name, item.unit, item.price] for item in Material.objects.all()]
    return render(request, "core/table.html", {
        "title": "Средства индивидуальной защиты",
        "headers": ["Код", "Наименование", "Ед.", "Цена"],
        "rows": rows,
        "add_url": "material_add",
    })


@login_required
def material_add(request):
    return save_form(request, MaterialForm, "Новое средство индивидуальной защиты", "materials")


@login_required
def specifications(request):
    items = Specification.objects.select_related("product")
    return render(request, "core/specifications.html", {"items": items})


@login_required
def specification_add(request):
    return save_form(request, SpecificationForm, "Новая норма обеспечения", "specifications")


@login_required
def specification_detail(request, pk):
    specification = get_object_or_404(Specification, pk=pk)
    form = SpecificationItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.specification = specification
        item.save()
        return redirect("specification_detail", pk=pk)
    return render(request, "core/specification_detail.html", {
        "specification": specification,
        "form": form,
    })


@login_required
def orders(request):
    items = Order.objects.select_related("customer")
    return render(request, "core/orders.html", {"items": items})


@login_required
def order_add(request):
    return save_form(request, OrderForm, "Новый инструктаж", "orders")


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.order = order
        item.save()
        return redirect("order_detail", pk=pk)
    return render(request, "core/order_detail.html", {"order": order, "form": form})


@login_required
def production_list(request):
    return render(request, "core/production.html", {"items": Production.objects.all()})


@login_required
def production_add(request):
    return save_form(request, ProductionForm, "Новая проверка условий труда", "production")


@login_required
def production_detail(request, pk):
    production = get_object_or_404(Production, pk=pk)
    product_form = ProductionProductForm(request.POST or None, prefix="product")
    material_form = ProductionMaterialForm(request.POST or None, prefix="material")
    if request.method == "POST":
        form = product_form if "add_product" in request.POST else material_form
        if form.is_valid():
            item = form.save(commit=False)
            item.production = production
            item.save()
            return redirect("production_detail", pk=pk)
    return render(request, "core/production_detail.html", {
        "production": production,
        "product_form": product_form,
        "material_form": material_form,
    })


@login_required
def cost_report(request):
    return render(request, "core/cost_report.html", {"orders": Order.objects.select_related("customer")})


@user_passes_test(lambda user: user.is_staff)
def users(request):
    rows = [[user.username, user.first_name or "-", "Да" if user.is_staff else "Нет"] for user in User.objects.all()]
    return render(request, "core/table.html", {
        "title": "Пользователи",
        "headers": ["Логин", "Имя", "Администратор"],
        "rows": rows,
    })


@login_required
def help_page(request):
    return render(request, "core/help.html")
