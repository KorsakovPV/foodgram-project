from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models import signals
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager, AbstractUser, Group, Permission


User = get_user_model()


# class UserAccountManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email address must be provided')
#
#         if not password:
#             raise ValueError('Password must be provided')
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email=None, password=None, **extra_fields):
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields['is_staff'] = True
#         extra_fields['is_superuser'] = True
#
#         return self._create_user(email, password, **extra_fields)
#
#
# class User(AbstractUser):#(AbstractBaseUser, PermissionsMixin):
#     pass
    # REQUIRED_FIELDS = []
    # USERNAME_FIELD = 'email'
    #
    # objects = UserAccountManager()
    #
    # email = models.EmailField('email', unique=True, blank=False, null=False)
    # full_name = models.CharField('full name', blank=True, null=True,
    #                              max_length=400)
    # is_staff = models.BooleanField('staff status', default=False)
    # is_active = models.BooleanField('active', default=True)
    #
    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name="user_set_groups",
    #     related_query_name="user",
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name=_('user permissions'),
    #     blank=True,
    #     help_text=_('Specific permissions for this user.'),
    #     related_name="user_set_user_permissions",
    #     related_query_name="user",
    # )
    #
    # def get_short_name(self):
    #     return self.email
    #
    # def get_full_name(self):
    #     return self.email
    #
    # def __unicode__(self):
    #     return self.email


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



