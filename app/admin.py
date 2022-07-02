from django.contrib import admin

# Register your models here.
from app.models import Category, Item, Profile, Order, RatingMark, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'location', 'birth_date', 'phone')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'status', 'created', 'updated', 'delivery_address', 'phone')


class RatingMarkAdmin(admin.ModelAdmin):
    list_display = ('mark',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','text','created','item','mark','user')
    list_display_links = ('id', 'text','item','mark','user')
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(RatingMark, RatingMarkAdmin)
admin.site.register(Comment, CommentAdmin)


