from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager
__all__ = [
    'Post',
]


class BaseModel(models.Model):
    """
    Базовый класс модели
    """
    objects = models.Manager()

    class Meta:
        abstract = True


class Post(BaseModel):
    h1 = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    url = models.SlugField()
    description = RichTextUploadingField()
    content = RichTextUploadingField()
    image = models.ImageField()
    created_at = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = TaggableManager()

    def __str__(self):
        return self.title
