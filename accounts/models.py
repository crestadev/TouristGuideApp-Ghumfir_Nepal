from django.db import models
from django.contrib.auth.models import User
from guides.models import Place

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')  # prevents duplicate favorites

    def __str__(self):
        return f"{self.user.username} -> {self.place.name}"
