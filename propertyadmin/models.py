from django.db import models
from .validators import FileValidator
from accounts.models import Account
from django.core.exceptions import ValidationError
import os, secrets

validate_file = FileValidator(max_size=1024 * 5000,
                             content_types=('image/jpeg','image/png','image/gif','image/tiff','application/x-empty',))


def image_path_handler(instance, filename):
    fn, ext = os.path.splitext(filename)
    #Create a random filename using hash function
    name = secrets.token_hex(20)
    print("uploading",instance.__dict__)
    return "property_{id}/{name}{ext}".format(id=instance.id,name=name,ext=ext)

def news_article_uploader(instance, filename):
    fn, ext = os.path.splitext(filename)
    return "news_{id}/{name}{ext}".format(id=instance.id,name=name,ext=ext)


class District(models.Model):
    code = models.CharField(max_length=5,null=False,unique=True)
    name = models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.code

class Property(models.Model):
    address_line_one = models.CharField(max_length=100,null=False)
    address_line_two = models.CharField(max_length=100,null=True,blank=True)
    town = models.CharField(max_length=60,null=False)
    postcode = models.CharField(max_length=30,null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    picture = models.ImageField(upload_to=image_path_handler,validators=[validate_file],null=True,blank=True)

    def __str__(self):
        return self.address_line_one

class Slot(models.Model):
    start_time =  models.TimeField(null=False)
    end_time =  models.TimeField(null=False)

class Customer(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name

class Agent(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.name


class Viewing(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    date_of_viewing = models.DateField(default=None)
    agent = models.ForeignKey(Agent,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)


    class Meta:
        unique_together = ('date_of_viewing', 'slot', 'property')

class NewsItem(models.Model):
    headline = models.CharField(max_length=50,null=False)
    article = models.CharField(max_length=500,null=False)
    picture = models.ImageField(upload_to=image_path_handler,validators=[validate_file],null=True,blank=True)
