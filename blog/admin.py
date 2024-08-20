from django.contrib import admin
from .models import Post, Category, Tag, Comment


class CategoryAdmin(admin.ModelAdmin):
    # 자동으로 채워지게 하는 필드
    prepopulated_fields = {"slug": ("name",)}


class TagAdmin(admin.ModelAdmin):
    # 자동으로 채워지게 하는 필드
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
