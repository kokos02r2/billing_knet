from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from .models import Group, TvIdentifier


class GroupAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_display = ('group_name', 'bandwidth', 'month_price')


admin.site.register(Group, GroupAdmin)
admin.site.register(TvIdentifier)
