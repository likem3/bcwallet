from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10
    ordering = ('-created_at',)