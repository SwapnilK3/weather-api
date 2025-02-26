from django.db import models
from django.core import validators

class DataSource(models.Model):
    region = models.CharField(max_length=100)
    parameter = models.CharField(max_length=100)
    order_statistic = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'

    def __str__(self):
        return self.region + ' - ' + self.parameter + ' - ' + self.order_statistic

class WeatherData(models.Model):
    year = models.IntegerField(
    validators=[
            validators.MinValueValidator(1800),
            validators.MaxValueValidator(2100)
        ])
    month = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ])
    value = models.FloatField()
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - {self.month}-{self.source}"