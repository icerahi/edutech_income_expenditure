import os

from django.conf import settings
from PIL import Image
from django.db import models

# Create your models here.
from django.db.models import Sum
from django.utils.safestring import mark_safe
from simple_history.models import HistoricalRecords
from smart_selects.db_fields import ChainedForeignKey


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Type, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '   Types'

class Source(models.Model):
    type = models.ForeignKey(Type,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = '  Source'

class Field(models.Model):
    type   = models.ForeignKey(Type,on_delete=models.CASCADE)
    source = ChainedForeignKey(Source, chained_field='type', chained_model_field='type',
                               show_all=False, auto_choose=True, sort=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = ' Fields'


#FILE   STORING
def file_name(instance,filename):
    ext = filename.split('.')[-1]
    filename=f'{instance.type}_{instance.field}_{instance.date}.'+ext
    return os.path.join(str(filename))

class TotalManager(models.Manager):
    def income(self):
        value=super(TotalManager, self).get_queryset().filter(type__name='income').aggregate(Sum('amount'))['amount__sum']
        if value is None:
            value=0
        return value
    def expense(self):
        value=super(TotalManager, self).get_queryset().filter(type__name='expense').aggregate(Sum('amount'))['amount__sum']
        if value is None:
            value=0

        return value

    def balance(self):
        return self.income()-self.expense()

class InEx(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    type = models.ForeignKey(Type,on_delete=models.SET_NULL,null=True,blank=True)
    source = ChainedForeignKey(Source,chained_field='type',chained_model_field='type',
                               show_all=False,auto_choose=True,sort=True)
    field = ChainedForeignKey(Field,chained_field='source',chained_model_field='source',
                               show_all=False,auto_choose=True,sort=True)
    note  = models.TextField()
    amount = models.FloatField()

    image = models.ImageField(help_text='allow only image',upload_to=file_name,null=True,blank=True)

    total  = TotalManager()
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history =  HistoricalRecords()


    def __str__(self):
        return self.note
    @mark_safe
    def image_tag(self):
        if self.image:
            return '<a href="{}"><img src="{}" style="width: 45px; height:35px;" /></a>'.format(self.image.url,self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'



    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'Income Expenditure'
        verbose_name = 'Income Expenditure'