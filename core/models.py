from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


POSITIVE_MONEY = [MinValueValidator(Decimal("0.00"))]
POSITIVE_QUANTITY = [MinValueValidator(Decimal("0.001"))]


class Customer(models.Model):
    """Сотрудник организации, проходящий мероприятия по охране труда."""

    source_id = models.CharField("Табельный номер", max_length=9, unique=True)
    name = models.CharField("ФИО", max_length=200)
    inn = models.CharField("СНИЛС", max_length=12, blank=True)
    address = models.TextField("Подразделение и должность", blank=True)
    phone = models.CharField("Телефон", max_length=20, blank=True)
    is_seller = models.BooleanField("Ответственный за охрану труда", default=False)
    is_buyer = models.BooleanField("Требуется контроль", default=True)

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    """Программа инструктажа или обучения по охране труда."""

    name = models.CharField("Наименование", max_length=200)
    code = models.CharField("Код программы", max_length=30, unique=True, blank=True, null=True)
    unit = models.CharField("Единица учета", max_length=20, default="курс")
    sale_price = models.DecimalField(
        "Плановая стоимость", max_digits=12, decimal_places=2, validators=POSITIVE_MONEY
    )

    class Meta:
        verbose_name = "программа обучения"
        verbose_name_plural = "программы обучения"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Material(models.Model):
    """Средство индивидуальной защиты или расходный материал."""

    name = models.CharField("Наименование", max_length=200)
    code = models.CharField("Номенклатурный код", max_length=30, unique=True, blank=True, null=True)
    unit = models.CharField("Единица измерения", max_length=20)
    price = models.DecimalField("Цена", max_digits=12, decimal_places=2, validators=POSITIVE_MONEY)

    class Meta:
        verbose_name = "СИЗ"
        verbose_name_plural = "средства индивидуальной защиты"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Specification(models.Model):
    """Норма обеспечения СИЗ для программы или вида работ."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Программа")
    name = models.CharField("Название нормы", max_length=200)
    is_active = models.BooleanField("Действует", default=True)

    class Meta:
        verbose_name = "норма обеспечения"
        verbose_name_plural = "нормы обеспечения"

    def __str__(self):
        return self.name

    def unit_material_cost(self):
        return sum(
            (item.quantity * item.material.price for item in self.items.select_related("material")),
            Decimal("0.00"),
        )


class SpecificationItem(models.Model):
    specification = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="items", verbose_name="Норма"
    )
    material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="СИЗ")
    quantity = models.DecimalField(
        "Количество по норме", max_digits=12, decimal_places=3, validators=POSITIVE_QUANTITY
    )

    class Meta:
        verbose_name = "позиция нормы"
        verbose_name_plural = "состав нормы"
        constraints = [
            models.UniqueConstraint(
                fields=["specification", "material"], name="unique_material_in_specification"
            )
        ]

    def __str__(self):
        return f"{self.material}: {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Запланирован"),
        ("work", "Проводится"),
        ("done", "Завершен"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name="Сотрудник")
    number = models.PositiveIntegerField("Номер")
    date = models.DateField("Дата")
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default="new")

    class Meta:
        verbose_name = "инструктаж"
        verbose_name_plural = "инструктажи"
        ordering = ["-date", "-number"]
        constraints = [models.UniqueConstraint(fields=["number", "date"], name="unique_order_number")]

    def __str__(self):
        return f"Инструктаж №{self.number} от {self.date:%d.%m.%Y}"

    def material_cost(self):
        total = Decimal("0.00")
        for item in self.items.select_related("product"):
            specification = item.product.specification_set.filter(is_active=True).first()
            if specification:
                total += item.quantity * specification.unit_material_cost()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Инструктаж")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Программа")
    quantity = models.DecimalField(
        "Количество сотрудников", max_digits=12, decimal_places=3, validators=POSITIVE_QUANTITY
    )
    unit_price = models.DecimalField(
        "Стоимость обучения", max_digits=12, decimal_places=2, validators=POSITIVE_MONEY
    )

    class Meta:
        verbose_name = "строка инструктажа"
        verbose_name_plural = "строки инструктажа"

    def __str__(self):
        return f"{self.product}: {self.quantity}"

    def sale_total(self):
        return self.quantity * self.unit_price


class Production(models.Model):
    number = models.PositiveIntegerField("Номер")
    date = models.DateField("Дата")

    class Meta:
        verbose_name = "проверка"
        verbose_name_plural = "проверки условий труда"
        ordering = ["-date", "-number"]

    def __str__(self):
        return f"Проверка №{self.number} от {self.date:%d.%m.%Y}"


class ProductionProduct(models.Model):
    production = models.ForeignKey(
        Production, on_delete=models.CASCADE, related_name="products", verbose_name="Проверка"
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Выявленный риск")
    quantity = models.DecimalField(
        "Количество замечаний", max_digits=12, decimal_places=3, validators=POSITIVE_QUANTITY
    )

    def __str__(self):
        return f"{self.product}: {self.quantity}"


class ProductionMaterial(models.Model):
    production = models.ForeignKey(
        Production, on_delete=models.CASCADE, related_name="materials", verbose_name="Проверка"
    )
    material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name="Рекомендованное СИЗ")
    quantity = models.DecimalField(
        "Количество", max_digits=12, decimal_places=3, validators=POSITIVE_QUANTITY
    )

    def __str__(self):
        return f"{self.material}: {self.quantity}"


class UserProfile(models.Model):
    ROLE_CHOICES = [("admin", "Администратор"), ("user", "Пользователь")]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField("Роль", max_length=10, choices=ROLE_CHOICES, default="user")
    is_blocked = models.BooleanField("Заблокирован", default=False)
    failed_attempts = models.PositiveSmallIntegerField("Ошибок входа", default=0)

    def __str__(self):
        return self.user.username
