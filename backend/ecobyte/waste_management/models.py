from django.db import models
from django.contrib.auth.models import User

class WasteItem(models.Model):
    CATEGORY_CHOICES = [
        ('Plastic', 'Plastic'),
        ('Paper', 'Paper'),
        ('Metal', 'Metal'),
        ('Organic', 'Organic'),
        ('E-Waste', 'E-Waste'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='waste_images/')
    waste_type = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.waste_type} - {self.user.username}"
