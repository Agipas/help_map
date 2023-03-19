from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'point')


class ImageInline(admin.TabularInline):
    model = Image


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_created', 'date_updated', 'author', 'cat')
    list_display_link = ('id', 'title')
    search_fields = ('title', 'content', 'author')
    prepopulated_fields = {'slug': ('title',)}

    inlines = [ImageInline]


admin.site.register(Point, PointAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Image, ImageAdmin)
# admin.site.register(Point, PointAdmin)
