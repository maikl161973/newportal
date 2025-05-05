from django.contrib.auth.models import User

from news_portal.models import (
    Author, Category, Post, NEWS, Comment, ARTICLE, PostCategory)

# запуск скрипта
# python manage.py shell < commands_django_shell.py


# Удалим чтобы можно было создать заново
Comment.objects.all().delete()
PostCategory.objects.all().delete()
Post.objects.all().delete()
Category.objects.all().delete()
Author.objects.all().delete()
User.objects.filter(username__in=('maikl', 'vlad', 'inna')).delete()


user_maikl = User.objects.create_user(username='maikl', password='111')
user_vlad = User.objects.create_user(username='vlad', password='222')
user_inna = User.objects.create_user(username='inna', password='333')

author_maikl = Author.objects.create(user=user_maikl)
author_vlad = Author.objects.create(user=user_vlad)

sport = Category.objects.create(name='Спорт')
polit = Category.objects.create(name='Политика')
educ = Category.objects.create(name='Образование')
health = Category.objects.create(name='Здоровье')

post_author_maikl_1 = Post.objects.create(
    author=author_maikl,
    title='Курсы python',
    content='Хорошие курсы по python у skillfactory',

)
post_author_maikl_2 = Post.objects.create(
    author=author_maikl,
    title='Куры Django',
    content='Курсы Django у skillfactory не плохие.',
)
post_author_vlad_1 = Post.objects.create(
    author=author_vlad,
    post_type=NEWS,
    title='Овечкин молодец',
    content='Забил ещё один красивый гол.',
)

post_author_maikl_1.category.add(educ)
post_author_maikl_1.category.add(polit)
post_author_vlad_1.category.add(sport)

comment_1 = Comment.objects.create(
    post=post_author_vlad_1,
    user=user_inna,
    comment='Отличная новость. Мне тоже нравится Овечкин')
comment_2 = Comment.objects.create(
    post=post_author_maikl_1,
    user=user_maikl,
    comment='A учу python в skillfactory')
comment_3 = Comment.objects.create(
    post=post_author_maikl_1,
    user=user_vlad,
    comment='Интересно!'
)
comment_4 = Comment.objects.create(
    post=post_author_maikl_2,
    user=user_maikl,
    comment='A учу Django в skillfactory. Это классно!')

post_author_maikl_1.like()
post_author_maikl_1.like()
post_author_maikl_1.dislike()

post_author_maikl_2.like()
post_author_maikl_2.like()
post_author_maikl_2.like()

comment_1.like()

comment_2.like()
comment_2.dislike()

comment_3.like()

comment_4.dislike()

author_maikl.update_rating()
author_vlad.update_rating()

print(f'Рейтинг Майкл: {author_maikl.rating}')
print(f'Рейтинг Влад: {author_vlad.rating}')

user_max_rating = Author.objects.order_by('-rating')[0]
print(f'Лучший пользователь: {user_max_rating.user.username}')

post_max_rating = Post.objects.filter(post_type=ARTICLE).order_by('-rating')[0]
print(
    f'Данные лучшего поста.  '
    f'дата: {post_max_rating.created}, '
    f'username автора: {post_max_rating.author.user.username}, '
    f'рейтинг: {post_max_rating.rating}, '
    f'заголовок: {post_max_rating.title}, '
    f'краткое содержание: {post_max_rating.preview()}')

comments = Comment.objects.filter(post=post_max_rating)
for comment in comments:
    print(
        f'дата:  {comment.created}, '
        f'пользователь: {comment.user.username}, '
        f'рейтинг: {comment.rating}, '
        f'комментарий: {comment.comment}'
    )
