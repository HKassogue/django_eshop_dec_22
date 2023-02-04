from django import template

register = template.Library()

@register.filter
def set_per(value, arg):
    """
    Replacing filter
    Use `{{ "value"|set_per:arg }}`
    """
    if len(value.split('per=')) != 2:
        return value

    value_without_nbr, val = value.split('per=')
    uri = value_without_nbr + 'per=' + str(arg)
    if '&' in val:
        uri += "&".join(val.split('&')[1:])
    return uri

@register.filter
def set_sort(value, arg):
    """
    Replacing filter
    Use `{{ "value"|set_sort:arg }}`
    """
    if len(value.split('sort=')) != 2:
        return value

    value_without_nbr, val = value.split('sort=')
    uri = value_without_nbr + 'sort=' + str(arg)
    if '&' in val:
        uri += "&".join(val.split('&')[1:])
    return uri