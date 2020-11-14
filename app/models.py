from django.db import models

# Create your models here.
from smart_selects.db_fields import ChainedForeignKey


class Type(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
class Source(models.Model):
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class InEx(models.Model):
    type = models.ForeignKey(Type,on_delete=models.DO_NOTHING)
    source = ChainedForeignKey(Source,chained_field='type',chained_model_field='type',
                               show_all=False,auto_choose=True,sort=True)
    note  = models.TextField()
    amount = models.DecimalField(max_digits=19,decimal_places=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.note

    class Meta:
        ordering = ['-updated']
        verbose_name_plural = 'Income Expenditure'