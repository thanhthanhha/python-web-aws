from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from pythonweb.storage_backends import PublicMediaStorage, PrivateMediaStorage

# Create your models here.
class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pic', storage=PublicMediaStorage())
    short_bio = models.CharField(max_length=100, default='short bio')
    long_bio = models.TextField(max_length=1000, default='long bio')
    job = models.CharField(max_length=100, default='Influencer')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

