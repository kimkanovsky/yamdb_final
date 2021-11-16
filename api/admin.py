from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

# @admin.register(Title)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = [field.name for field
#                     in Title._meta.fields if field.name != "id"]


# @admin.register(Genre)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = [field.name for field
#                     in Genre._meta.fields if field.name != "id"]


# @admin.register(Category)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = [field.name for field
#                     in Category._meta.fields if field.name != "id"]


# @admin.register(Review)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = [field.name for field
#                     in Review._meta.fields if field.name != "id"]


# @admin.register(Comment)
# class TitleAdmin(admin.ModelAdmin):
#     list_display = [field.name for field
#                     in Comment._meta.fields if field.name != "id"]


admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Comment)
