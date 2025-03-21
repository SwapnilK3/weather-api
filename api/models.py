from django.db import models
from django.core import validators

class DataSource(models.Model):
    region = models.CharField(max_length=100)
    parameter = models.CharField(max_length=100)
    # parameter = models.CharField(
    #     max_length=100,
    #     choices=[
    #         ('Tmax', 'Maximum Temperature'),
    #         ('Tmin', 'Minimum Temperature'),
    #         ('Tmean', 'Mean Temperature'),
    #         ('Rainfall', 'Rainfall'),
    #         ('Sunshine', 'Sunshine Hours'),
    #         ('Airfrost', 'Air Frost Days'),
    #         ('Raindays', 'Rain Days'),
    #     ])
    
    
    order_statistic = models.CharField(
        max_length=100,
        choices=[('date', 'Date'), ('ranked', 'Ranked')]
        )

    class Meta:
        unique_together = ('region', 'parameter', 'order_statistic')
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
        indexes = [
            models.Index(fields=['region']),
            models.Index(fields=['parameter']),
        ]

    def __str__(self):
        return self.region + ' - ' + self.parameter + ' - ' + self.order_statistic

class WeatherData(models.Model):
    year = models.IntegerField(
    validators=[
            validators.MinValueValidator(1800),
            validators.MaxValueValidator(2100)
        ],
    help_text="Year of the weather record (1800-2100)"
    )
    month = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ])
    value = models.FloatField()
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
        
    @property
    def month_name(self):
        """Returns the month name (January, February, etc.)"""
        import calendar
        return calendar.month_name[self.month]
    
    @property
    def season(self):
        """Returns the meteorological season for the record"""
        if self.month in [12, 1, 2]:
            return "Winter"
        elif self.month in [3, 4, 5]:
            return "Spring"
        elif self.month in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"
    
    def __str__(self):
        return f"{self.year} - {self.month}-{self.source}"
    
    class Meta:
        indexes = [
            models.Index(fields=['year', 'month']),
            models.Index(fields=['source']),
            models.Index(fields=['year']),
        ]
        
        constraints = [
                models.UniqueConstraint(
                    fields=['year', 'month', 'source'], 
                    name='unique_weather_record'
                ),
            ]