from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Group, TvIdentifier


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'tv_identifiers': FilteredSelectMultiple("TV Identifiers", is_stacked=False),
        }


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ('group_name', 'bandwidth', 'month_price')


admin.site.register(Group, GroupAdmin)
admin.site.register(TvIdentifier)
