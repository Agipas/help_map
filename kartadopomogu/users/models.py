from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserModel(AbstractUser):
    STATUS = (
        ('volonter', 'Волонтер'),
        ('viskovui', 'Військовослужбовець')
    )
    VERIFICATION = (
        ('not_verified', 'Не перевірений'),
        ('processing', 'В обробці'),
        ('verified', 'Перевірений')
    )
    bio = models.TextField(max_length=2000, blank=False)
    avatar = models.ImageField(upload_to='users/', blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, blank=False)
    phone_number = PhoneNumberField(blank=True)
    is_verified = models.CharField(max_length=100, choices=VERIFICATION, blank=False, default='not_verified')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)
