import os.path

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.conf import settings


class Point(models.Model):
    class Meta:
        verbose_name = "Допомогa"
        verbose_name_plural = "Допомоги"
        ordering = ["-date_updated"]

    title = models.CharField(max_length=200, db_index=True, verbose_name="Назва")
    content = models.TextField(max_length=5000, verbose_name="Інформація")
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, verbose_name="Категорія")
    point_url = models.CharField(max_length=250, unique=True, null=False, verbose_name="Посилання")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('point_info', kwargs={'point_slug': self.slug})


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


# def point_directory_path(instance, filename):
#     base_name = os.path.basename(filename)
#     name, ext = os.path.splitext(base_name)
#
#     return "point/" + str(instance.point.id) + "/"+"IMG_" + str(instance.point.id)+ext


class Image(models.Model):
    class Meta:
        verbose_name = "Фотографія"
        verbose_name_plural = "Фотографії"
        ordering = ["point"]

    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    # image = models.ImageField(upload_to=point_directory_path, null=True, blank=True)

    def __str__(self):
        return "{}: {}".format(self.point.title, str(self.image))
