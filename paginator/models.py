from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField

class Paginator(models.Model):
    paginator_title = models.CharField(max_length=100)
    paginator_des= HTMLField()
    # paginator_slug = AutoSlugField(populate_from='paginator_title',unique=True,null=True,default=None)
    
    

# Create your models here.
