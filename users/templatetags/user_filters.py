from django import template

register = template.Library()


@register.filter
def url_with_get(request, page):
    query = request.GET.copy()
    query['page'] = page
    return query.urlencode()


#TODO теги уже хранятся в базе как абстрактные строчки, а тут - прибитый
# гвоздями к коду список тегов и их соответствие цветам (читай - словарь
# строка:строка). Намного лучше и дальше поддерживать хороший подход, не
# фиксируя какие-то определенные детали. Например, можно вынести цвет тоже в
# базу
@register.filter
def add_color(tag):
    colors = {
        'breakfast': 'orange',
        'lunch': 'green',
        'dinner': 'purple'
    }
    return colors[tag.slug]


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def subtract(number_1, number_2):
    return int(number_1) - int(number_2)


@register.filter
def get_tags(request):
    return request.getlist('tag')


@register.filter
def renew_tag_link(request, tag):
    request_copy = request.GET.copy()
    tags = request_copy.getlist('tag')
    if tag.slug in tags:
        tags.remove(tag.slug)
        request_copy.setlist('tag', tags)
    else:
        request_copy.appendlist('tag', tag.slug)
    return request_copy.urlencode()
