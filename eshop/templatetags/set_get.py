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