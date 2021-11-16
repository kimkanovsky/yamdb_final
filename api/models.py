import datetime as dt
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import (AbstractUser,
                                        BaseUserManager)
from django.core.exceptions import ValidationError
from django_utils.choices import Choice, Choices
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import AccessToken


class RoleChoices(Choices):
    USER = Choice('user', _('user'))
    MODERATOR = Choice('moderator', _('moderator'))
    ADMIN = Choice('admin', _('admin'))


# Вот ради одной функции точно не буду новый файл создавать
def my_year_validator(value):
    if value > dt.datetime.now().year:
        raise ValidationError(
            _('%(value)s is not a correct year!'),
            params={'value': value},
        )


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(
            email,
            username,
            password,
        )
        user.username = username
        user.is_admin = True
        user.role = RoleChoices.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    username = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Имя пользователя'
    )
    bio = models.CharField(
        max_length=255, blank=True, verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        max_length=10,
        choices=RoleChoices.choices,
        default='user',
        verbose_name='Роль пользователя')
    password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Пароль пользователя'
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'

    NAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id', ]

    def set_password(self, raw_password):
        super().set_password(raw_password)

    def __str__(self):
        return self.email

    def _generate_jwt_token(self):
        token = AccessToken.for_user(self)
        return token

    @property
    def role_is_user(self):
        return self.role == RoleChoices.USER

    @property
    def role_is_moderator(self):
        return self.role == RoleChoices.MODERATOR

    @property
    def role_is_admin(self):
        return self.role == RoleChoices.ADMIN


class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['name'], name='unique_genre_name'
            ),
            models.constraints.UniqueConstraint(
                fields=['slug'], name='unique_genre_slug'
            ),
        ]
        ordering = ['-id', ]
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['name'], name='unique_category_name'
            ),
            models.constraints.UniqueConstraint(
                fields=['slug'], name='unique_category_slug'
            ),
        ]
        ordering = ['-id', ]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    year = models.IntegerField(null=True, verbose_name='Год выпуска',
                               validators=[my_year_validator])
    description = models.TextField(null=True, verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        db_column='category',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.constraints.UniqueConstraint(
                fields=['name'], name='unique_title_name'
            )
        ]

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='author'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(
                0,
                message='Убедитесь, что это значение больше или равно 0'),
            MaxValueValidator(
                11,
                message='Убедитесь, что это значение меньше или равно 10')]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-id', ]
        verbose_name = 'Ревью'
        verbose_name_plural = 'Ревью'

    def __str__(self) -> str:
        return f'{self.score}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='author'

    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True
    )

    class Meta:
        ordering = ['-id', 'pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
