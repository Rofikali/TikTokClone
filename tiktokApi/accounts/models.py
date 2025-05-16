from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from core.models import AutoUpdate


class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# class AutoUpdate(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    """

    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="user_images/", blank=True, null=True, default="default.jpg"
    )
    email = models.EmailField(unique=True)  # Email as the unique identifier
    username = models.CharField(
        max_length=150, unique=False, blank=True, null=True
    )  # Make username optional
    name = models.CharField(max_length=255, blank=True, null=True)

    # Custom manager
    objects = CustomUserManager()

    USERNAME_FIELD = "email"  # Use email as the primary identifier
    REQUIRED_FIELDS = ["username"]  # Required fields when creating a superuser

    def __str__(self):
        return self.email


class Post(AutoUpdate):
    # user = models.ForeignKey('api.User', on_delete=models.CASCADE)  # Use 'api.User'
    user = models.ForeignKey(
        User,  # Refers to the custom User model
        on_delete=models.CASCADE,
        related_name="posts",  # Reverse relationship (user.posts.all())
    )
    text = models.TextField()
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.text}"

    class Meta:
        ordering = ["-created_at"]  # Latest posts appear first
