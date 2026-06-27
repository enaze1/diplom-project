from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Customer, Material, Order, OrderItem, Product, Specification, SpecificationItem


class CostCalculationTest(TestCase):
    def test_order_material_cost(self):
        employee = Customer.objects.create(source_id="000000001", name="Иванов Сергей Петрович")
        program = Product.objects.create(name="Первичный инструктаж", unit="курс", sale_price=0)
        ppe = Material.objects.create(name="Каска защитная", unit="шт", price=650)
        specification = Specification.objects.create(product=program, name="Норма выдачи СИЗ")
        SpecificationItem.objects.create(specification=specification, material=ppe, quantity=Decimal("1.0"))
        order = Order.objects.create(customer=employee, number=1, date=date.today())
        OrderItem.objects.create(order=order, product=program, quantity=2, unit_price=0)

        self.assertEqual(order.material_cost(), Decimal("1300.00"))


class PageAccessTest(TestCase):
    def test_dashboard_is_available_after_login(self):
        user = User.objects.create_user(username="student", password="test-password")
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
