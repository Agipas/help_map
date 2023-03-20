import os.path
import string
from random import random

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField
# from geoposition.fields import GeopositionField


class Point(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Point", slugify(self.slug), instance)

    def default_slug(self, instance=None):
        if instance:
            return slugify(self.title.join(random.sample(string.ascii_lowercase, 10)))

    class Meta:
        verbose_name = "Допомогa"
        verbose_name_plural = "Допомоги"
        ordering = ["-date_updated"]

    title = models.CharField(max_length=200, db_index=True, verbose_name="Назва", unique=True)
    content = HTMLField(blank=True, default="", verbose_name="Інформація")
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    slug = models.SlugField(max_length=100, default=default_slug)
    is_published = models.BooleanField(default=False)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категорія")
    point_url = models.CharField(max_length=250, unique=True, null=False, verbose_name="Посилання")
    photo = models.ImageField(default='default/no_image.jpeg', upload_to=image_upload_to)
    # position = GeopositionField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('point_info', kwargs={'point_slug': self.slug})

    def get_update_url(self):
        return reverse('point_update', kwargs={'point_slug': self.slug})

    def save(self, *args, **kwargs):
        super(Point, self).save(*args, **kwargs)
        return self


class Category(models.Model):
    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})

    def get_user_absolute_url(self):
        return reverse('category', kwargs={"cat_slug": self.slug})


def point_directory_path(instance, filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)

    return "point/" + str(instance.point.id) + "/"+"IMG_" + str(instance.point.id)+ext


class Image(models.Model):
    class Meta:
        verbose_name = "Фотографія"
        verbose_name_plural = "Фотографії"
        ordering = ["point"]

    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    image = models.FileField(upload_to=point_directory_path, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.point.title, str(self.image))
