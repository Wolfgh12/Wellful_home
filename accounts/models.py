from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SENIOR = 'SENIOR', 'Senior / End User'
        CAREGIVER = 'CAREGIVER', 'Caregiver / Family'
        ADMIN = 'ADMIN', 'Store Administrator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.SENIOR,
    )
    phone_number = models.CharField(max_length=20, blank=True, default="")
    digital_address = models.CharField(
        max_length=50, 
        blank=True, 
        default="", 
        help_text="GhanaPost GPS Address"
    )

    @property
    def is_senior(self):
        return self.role == self.Role.SENIOR

    @property
    def is_caregiver(self):
        return self.role == self.Role.CAREGIVER

    @property
    def is_store_admin(self):
        return self.role == self.Role.ADMIN

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"