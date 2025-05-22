from django import template

register = template.Library()

BAD_WORDS = ['дурак', 'балбес', 'кретин']


@register.filter()
def cencor(value):
    for bad_word in BAD_WORDS:
       value = value.replace(
          bad_word,'{}{}'.format(bad_word[0], '*' * (len(bad_word) - 1)))
    return value

