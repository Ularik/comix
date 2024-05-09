from django.contrib.auth import get_user_model
from django.db import models
User = get_user_model()


class Posters(models.Model):
    image = models.ImageField(
        upload_to='comix/images',
        null=True,
        blank=True
    )


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comix = models.ForeignKey(
        'Comix',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    grade = models.IntegerField(
        choices=(
            (10, 10),
            (9, 9),
            (8, 8),
            (7, 7),
            (6, 6),
            (5, 5),
            (4, 4),
            (3, 3),
            (2, 2),
            (1, 1),
        )
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )


class Likes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    comix = models.ForeignKey(
        'Comix',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user} -> {self.comix}'


class Comments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    comix = models.ForeignKey(
        'Comix',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=100
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Genre(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='comix/images/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Comix(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    chapters = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    pages = models.PositiveIntegerField(    # will automatically fill after first read in comix_detail
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(Genre)
    comix_file = models.FileField(
        upload_to='comix/',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='comix/images/',
        null=True,
        blank=True
    )
    watches = models.PositiveIntegerField(default=1)
    common_grade = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Bookmarks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    comix = models.ForeignKey(
        Comix,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.user.username}: {self.comix.title}'
