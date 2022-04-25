from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'MEDIA/user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="user")
    profile_picture = models.ImageField(upload_to=user_directory_path, default='user.png')
    online = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'
    def __str__(self):
        return self.user.username

    def save(self,  *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)
        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)