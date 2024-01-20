from django.contrib import admin
from django.db import models
from .models import Group, TvIdentifier
from django.forms import CheckboxSelectMultiple


class GroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_display = ('group_name', 'bandwidth', 'month_price')


admin.site.register(Group, GroupAdmin)
admin.site.register(TvIdentifier)
