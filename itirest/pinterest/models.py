from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class Cast(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    class Meta:
        ordering = ('firstname',)


class CommonInfo(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    release_date = models.DateField()
    categories = models.ManyToManyField(Category)
    cast = models.ManyToManyField(Cast)
    poster_image = models.ImageField(upload_to='pinterest_posters')
    watch_count = models.IntegerField()
    likes = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Movie(CommonInfo):
    pass


class Series(CommonInfo):
    season = models.CharField(max_length=50)
    episode = models.CharField(max_length=50)
