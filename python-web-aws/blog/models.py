from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from pythonweb.storage_backends import PublicMediaStorage, PrivateMediaStorage

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='post_pic', storage=PublicMediaStorage())
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(200, 200)],
                                     format='JPEG',
                                     options={'quality': 1000})

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    content = models.TextField()
    created_date =  models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} comment on {self.post.title}'
class Like(models.Model):
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    comment= models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='cmt_like', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user} likes {self.post}'