from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from rentify.settings import AUTH_USER_MODEL


class RentifyUserManager(UserManager):
    def _create_user(self, email, password, **extra_args):
        if not email:
            raise ValueError("Email is required to create a user")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_args)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, role=None, password=None, **extra_args):
        extra_args.setdefault("is_staff", False)
        extra_args.setdefault("is_superuser", False)
        if not role or role not in ["buyer", "seller"]:
            role = "buyer"

        extra_args.setdefault("role", role)

        return self._create_user(email, password, **extra_args)

    def create_superuser(self, email, password=None, **extra_args):
        extra_args.setdefault("is_staff", True)
        extra_args.setdefault("is_superuser", True)
        extra_args.setdefault("role", "admin")

        if extra_args.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_args.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_args)


class User(AbstractUser):

    username = None

    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=6,
        choices=(
            ("admin", "Adminstrator"),
            ("buyer", "Buyer"),
            ("seller", "Seller"),
        ),
        default="buyer",
    )
    contact = models.CharField(max_length=13)

    objects = RentifyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["contact"]

    class Meta:
        unique_together = ("first_name", "last_name")

    def __str__(self):
        return self.email

    def clean(self):
        if not self.is_superuser and self.role == "admin":
            raise ValidationError(
                {"role": _("Selected role cannot be assigned to the user.")}
            )
