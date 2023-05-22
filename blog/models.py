from django.db import models
from django.utils.html import format_html
from account.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from extensions.utlis import diffNowDate

# Create your models here.
class category (models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(null=True)

class post (models.Model):
    image = models.ImageField(upload_to='blog/',default='blog/default.jpg')
    author = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name='articles')
    title =models.CharField(max_length= 255)
    content = models.TextField()
    tags = TaggableManager()
    category =models.ManyToManyField(category)
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    counted_view=models.IntegerField(null=False, default=0) 
    class Meta:
        ordering = ['-created_date']
    def diftimes(self):
        return diffNowDate(self.published_date)

    def __str__(self) :
        return "{} - {}" .format(self.title,self.id) 
    def get_absolute_url(self):
        return reverse("account:home")
    # def get_absolute_url (self):
    #     return reverse('blog:single',kwargs={'pid':self.id})

    def image_tag (self):
        return format_html("<img width=100 height=75 src='{}'>".format(self.image.url))

class Newsletter(models.Model):
    email =models.EmailField()
    def __str__(self) :
        return self.email