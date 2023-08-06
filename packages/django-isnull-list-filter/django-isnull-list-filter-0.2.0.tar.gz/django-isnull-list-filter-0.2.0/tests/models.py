from django.db import models


class Author(models.Model):
    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    name = models.TextField()


class Album(models.Model):
    author = models.ForeignKey(
        Author,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    coauthors = models.ManyToManyField(
        Author,
        null=True,
        blank=True,
        related_name="coauthored_albums",
    )
    released = models.DateField(
        null=True,
        blank=True,
    )


class Song(models.Model):
    album = models.ForeignKey(
        Album,
        related_name="song_set",
        on_delete=models.CASCADE,
    )
