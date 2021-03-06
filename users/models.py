from django.contrib.auth import get_user_model

from django.db import models

User = get_user_model()


class Subscription(models.Model):
    """Описание модели для реализации подписок"""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')

    class Meta:
        unique_together = ('user', 'author',)

    def __str__(self):
        return f'{self.user} подписан на {self.author}.'
