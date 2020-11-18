from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, ImageField, DateField, Manager
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for Art For Introvert backend.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = EmailField(_('email address'), unique=True)
    userpic = ImageField(_('userpic'),
                         upload_to='user_userpics/',
                         null=True,
                         blank=True)
    birthdate = DateField(_("Birth Date"), blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"User #{self.id}: {self.email}"

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
