from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='static/profile_pic')
    photo_id = models.ImageField(upload_to='static/photo_id')
    DOB = models.DateField() # must be 18 years or older
    address = models.CharField(max_length=200)
    is_donor = models.BooleanField(default=True)
    name = models.CharField(max_length = 90, null = False, default = '')
    def clean(self):
        age = timezone.now().date().year - self.DOB.year - ((timezone.now().date().month, timezone.now().date().day) < (self.DOB.month, self.DOB.day))
        if age < 18:
            raise ValidationError("Users must be 18 years or older to register.")

    def __str__(self):
        return self.user.username

class Food(models.Model):
    provider = models.ForeignKey(User, related_name='provided_foods', on_delete=models.CASCADE)
    taker = models.ForeignKey(User, related_name='taken_foods', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='food_images/')
    TYPE_CHOICES = [
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('OTHER', 'Other'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    WEIGHT_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]
    weight = models.CharField(max_length=1, choices=WEIGHT_CHOICES)
    expiry_date = models.DateField(blank=True, null=True)
    desc = models.TextField()
    postal_code = models.CharField(max_length=6)
    status = models.BooleanField(default=True)
    cooked_time = models.DateTimeField()
    carbon_emission = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.calculate_carbon_emission()
        super().save(*args, **kwargs)

    def calculate_carbon_emission(self):
        emission_factors = {
            'VEG': {
                'S': 0.5,
                'M': 0.7,
                'L': 1.0,
            },
            'NON_VEG': {
                'S': 1.0,
                'M': 1.5,
                'L': 2.0,
            },
            'OTHER': {
                'S': 0.8,
                'M': 1.2,
                'L': 1.6,
            }
        }
        emission_factor = emission_factors.get(self.type, {}).get(self.weight)
        if emission_factor is not None:
            weight_values = {'S': 0.5, 'M': 1.0, 'L': 1.5} 
            weight = weight_values.get(self.weight)
            if weight is not None:
                self.carbon_emission = emission_factor * weight
            else:
                self.carbon_emission = None
        else:
            self.carbon_emission = None

    def __str__(self):
        return f'Provied by {self.provider} to: {self.taker}'