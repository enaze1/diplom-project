from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import (
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
    UserProfile,
)


class Command(BaseCommand):
    help = "Создает учебные данные для системы охраны труда"

    def handle(self, *args, **options):
        ProductionMaterial.objects.all().delete()
        ProductionProduct.objects.all().delete()
        Production.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        SpecificationItem.objects.all().delete()
        Specification.objects.all().delete()
        Material.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()

        admin, _ = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("admin123")
        admin.save()
        UserProfile.objects.update_or_create(user=admin, defaults={"role": "admin"})

        student, _ = User.objects.get_or_create(username="student")
        student.set_password("student123")
        student.save()
        UserProfile.objects.update_or_create(user=student, defaults={"role": "user"})

        employees = [
            ("000000001", "Иванов Сергей Петрович", "12345678901", "Производственный участок, слесарь", "+79198634592", False, True),
            ("000000002", "Петрова Анна Викторовна", "22345678901", "Склад, кладовщик", "+79884581555", False, True),
            ("000000003", "Смирнов Олег Игоревич", "32345678901", "Электроцех, электромонтер", "+79882584546", False, True),
            ("000000004", "Кузнецова Мария Андреевна", "42345678901", "Администрация, специалист по ОТ", "+79627486389", True, False),
            ("000000005", "Соколова Елена Павловна", "52345678901", "Лаборатория, инженер", "+79184572398", False, True),
        ]
        for source_id, name, snils, position, phone, responsible, control in employees:
            Customer.objects.update_or_create(source_id=source_id, defaults={
                "name": name,
                "inn": snils,
                "address": position,
                "phone": phone,
                "is_seller": responsible,
                "is_buyer": control,
            })

        program_data = [
            ("Вводный инструктаж по охране труда", "ОТ-001", "курс", "0.00"),
            ("Первичный инструктаж на рабочем месте", "ОТ-002", "курс", "0.00"),
            ("Обучение безопасным методам работ на высоте", "ОТ-003", "курс", "3500.00"),
            ("Пожарно-технический минимум", "ОТ-004", "курс", "2500.00"),
        ]
        programs = {}
        for name, code, unit, price in program_data:
            program, _ = Product.objects.update_or_create(name=name, defaults={
                "code": code,
                "unit": unit,
                "sale_price": Decimal(price),
            })
            programs[name] = program

        helmet, _ = Material.objects.update_or_create(name="Каска защитная", defaults={
            "code": "СИЗ-001", "unit": "шт", "price": Decimal("650.00"),
        })
        gloves, _ = Material.objects.update_or_create(name="Перчатки защитные", defaults={
            "code": "СИЗ-002", "unit": "пара", "price": Decimal("180.00"),
        })
        goggles, _ = Material.objects.update_or_create(name="Очки защитные", defaults={
            "code": "СИЗ-003", "unit": "шт", "price": Decimal("320.00"),
        })

        specification, _ = Specification.objects.update_or_create(
            product=programs["Первичный инструктаж на рабочем месте"],
            defaults={"name": "Норма выдачи СИЗ для производственного участка", "is_active": True},
        )
        SpecificationItem.objects.update_or_create(
            specification=specification, material=helmet, defaults={"quantity": Decimal("1.000")}
        )
        SpecificationItem.objects.update_or_create(
            specification=specification, material=gloves, defaults={"quantity": Decimal("2.000")}
        )
        SpecificationItem.objects.update_or_create(
            specification=specification, material=goggles, defaults={"quantity": Decimal("1.000")}
        )

        employee = Customer.objects.get(source_id="000000001")
        order, _ = Order.objects.update_or_create(
            number=1,
            date=date(2026, 6, 23),
            defaults={"customer": employee, "status": "done"},
        )
        OrderItem.objects.update_or_create(
            order=order,
            product=programs["Первичный инструктаж на рабочем месте"],
            defaults={"quantity": Decimal("1.000"), "unit_price": Decimal("0.00")},
        )

        inspection, _ = Production.objects.get_or_create(number=1, date=date(2026, 6, 24))
        ProductionProduct.objects.update_or_create(
            production=inspection,
            product=programs["Обучение безопасным методам работ на высоте"],
            defaults={"quantity": Decimal("1.000")},
        )
        ProductionMaterial.objects.update_or_create(
            production=inspection, material=helmet, defaults={"quantity": Decimal("1.000")}
        )
        ProductionMaterial.objects.update_or_create(
            production=inspection, material=gloves, defaults={"quantity": Decimal("2.000")}
        )

        self.stdout.write(self.style.SUCCESS("Данные созданы. Логин: admin, пароль: admin123"))
