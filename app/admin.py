from django.contrib import admin

# Register your models here.
from app.models import InEx, Type, Source
@admin.register(InEx)
class InExAdmin(admin.ModelAdmin):
    list_display = ('type','source','note','amount','created')
    search_fields = ('note','created','amount')
    list_filter = ('type','source',)\

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('name','type')




admin.site.site_header="Edutech Income Expenditure"
admin.site.site_title ="Edutech Income Expenditure"
admin.site.index_title = "Edutech Income Expenditure"
