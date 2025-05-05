from django.db import models
from django.contrib.auth.models import User


ARTICLE = 1
NEWS = 2

POST_TYPES = (
    (ARTICLE, 'Статья'),
    (NEWS, 'Новость')
)


class Author(models.Model):
    """Автор"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

    def update_rating(self):
        article_sum = (
            self.post_set.filter(
                post_type=ARTICLE
            ).aggregate(models.Sum('rating'))['rating__sum'] or 0) * 3
        autor_write_comment_sum = Comment.objects.filter(
            user=self.user
        ).aggregate(models.Sum('rating'))['rating__sum'] or 0

        by_autor_comment = Comment.objects.filter(
            post__author=self
        ).aggregate(models.Sum('rating'))['rating__sum'] or 0

        self.rating = sum([
            article_sum, autor_write_comment_sum, by_autor_comment])


class Category(models.Model):
    """Категория"""
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    """Пост"""

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.SmallIntegerField(choices=POST_TYPES, default=ARTICLE)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating == 0:
            return

        self.rating -= 1
        self.save()

    def preview(self):
        return  f'{str(self.content).strip()}...'

class PostCategory(models.Model):
    """Связь пост и категории"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)



class Comment(models.Model):
    """Комментарий"""

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating == 0:
            return

        self.rating -= 1
        self.save()

