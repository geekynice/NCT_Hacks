from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    photo_id = models.ImageField(upload_to='photo_id/')
    DOB = models.DateField() # must be 18 years or older
    address = models.CharField(max_length=200)
    is_donor = models.BooleanField(default=True)

    def clean(self):
        age = timezone.now().date().year - self.DOB.year - ((timezone.now().date().month, timezone.now().date().day) < (self.DOB.month, self.DOB.day))
        if age < 18:
            raise ValidationError("Users must be 18 years or older to register.")

    def __str__(self):
        return self.user.username
    
# class Food(models.Model):
#     image = models.ImageField(upload_to='profile_pic/')
#     type = 
#     category = 
#     weight = option
#     expiry date(optional)
#     desc = 