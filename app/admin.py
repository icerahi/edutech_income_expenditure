from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from import_export.fields import Field
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from simple_history.admin import SimpleHistoryAdmin

from app.models import InEx, Type, Field

class InExResource(resources.ModelResource):
    class Meta:
        model = InEx
        fields =('type__name','field','note','amount','date')


@admin.register(InEx)
class InExAdmin(ImportExportModelAdmin,SimpleHistoryAdmin):
    #change_list_template = 'admin/import_export/change_list.html'
    history_list_display = ["amount"]
    list_display = ('type','field','note','amount','date','image_tag',)
    search_fields = ('note','date','amount')
    date_hierarchy = 'date'
    resource_class = InExResource
    fields = ('type','field','note','amount','image',)
    readonly_fields = ['image_tag']

    list_filter = (
        ('date', DateRangeFilter),('type'),('created_by__username'),('field'),
    )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(InExAdmin, self).save_model(request,obj,form,change)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['income'] = InEx.total.income()
        extra_context['expense'] = InEx.total.expense()
        extra_context['balance'] = InEx.total.balance()
        return super(InExAdmin, self).changelist_view(request, extra_context=extra_context)




@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Field)
class SourceAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('name','type')




admin.site.site_header="EduTech System Ltd."
admin.site.site_title ="Edutech Income Expenditure"
admin.site.index_title = "Edutech Income Expenditure"
