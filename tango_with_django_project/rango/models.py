from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
MAX_LENGTH = 128
class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, unique=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    def __str__(self):
        return self.title