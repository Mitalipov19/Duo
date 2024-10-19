from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, null=True, blank=True,
                                           validators=[MinValueValidator(11), MaxValueValidator(110)])
    phone_number = PhoneNumberField(null=True, blank=True, region='KG')

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Marka(models.Model):
    marka_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.marka_name


class Model(models.Model):
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=16)

    def __str__(self):
        return f'{self.marka}-{self.model_name}'


class Car(models.Model):
    marka = models.ForeignKey(Marka, related_name='products', on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.PositiveSmallIntegerField(default=0)
    year = models.DateField()
    mileage = models.IntegerField(default=0, verbose_name='пробег')
    body = models.CharField(max_length=32, verbose_name='кузов')
    color = models.CharField(max_length=32)
    ENGINE_CHOICES = (
        ('бензин', 'бензин'),
        ('дизель', 'дизель'),
        ('газ', 'газ'),
        ('электрический', 'электрический'),
        ('гибрид', 'гибрид')
    )
    engine_type = models.CharField(choices=ENGINE_CHOICES, max_length=16, verbose_name='двигатель')
    GEARBOX_CHOICES = (
        ('Механическая', 'Механическая'),
        ('Автоматическая', 'Автоматическая'),
        ('Трансмиссия', 'Трансмиссия'),
        ('Полуавтоматическая', 'Полуавтоматическая'),
        ('Полуавтоматическая', 'Полуавтоматическая')
    )
    gearboxes_type = models.CharField(choices=GEARBOX_CHOICES, max_length=32, verbose_name='каробка')
    DRIVE_CHOICES = (
        ('передный', 'передный'),
        ('задный', 'задный'),
        ('полный', 'полный')
    )
    drive_type = models.CharField(choices=DRIVE_CHOICES, max_length=16, verbose_name='привод')
    STEERING_CHOICES = (
        ('слева', 'слева'),
        ('справа', 'справа')
    )
    Steering_wheel = models.CharField(choices=STEERING_CHOICES, max_length=10, verbose_name='руль')
    description = models.TextField()
    STATE_CHOICES = (
        ('хорошее', 'хорошее'),
        ('идеальное', 'идеальное'),
        ('аварийное', 'аварийное'),
        ('новое', 'новое')
    )
    state = models.CharField(choices=STATE_CHOICES, max_length=16, verbose_name='состояние')
    region = models.CharField(max_length=32, verbose_name='регион/город продажи')
    active = models.BooleanField(default=True, verbose_name='в наличии')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.marka}-{self.model}'


class CarPhotos(models.Model):
    car = models.ForeignKey(Car, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_image/')


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='comment', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}-{self.car}'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)