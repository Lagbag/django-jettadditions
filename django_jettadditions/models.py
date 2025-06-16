from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[('admin', 'Administrator'), ('user', 'User')])
    is_blocked = models.BooleanField(default=False)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)

    class Meta:
        db_table = 'custom_user'

class Premise(models.Model):
    name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'premises'

class Client(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    class Meta:
        db_table = 'clients'

class Rental(models.Model):
    premise = models.ForeignKey(Premise, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'rentals'