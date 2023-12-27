from django.contrib import admin
from .models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'bandwidth', 'month_price')


admin.site.register(Group, GroupAdmin)
