from django.db import models

# Create your models here.

class Books(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_date = models.DateField()

    class Meta:
        verbose_name_plural = "Books"

    def __str__(self):
        return self.title
