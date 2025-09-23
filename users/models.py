from django.db import models
from django.contrib.auth.models import User

class ProfileImg(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_img')
    image = models.ImageField(upload_to="profile_images/", default='imgs/default.jpg')
    
    def __str__(self):
        return f"{self.user.username} profile image"