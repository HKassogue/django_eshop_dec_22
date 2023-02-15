from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(is_safe=True)
def format_rate(rate):
    code = ''
    # if rate < 1/2: 
    #     code += '<i class="far fa-star text-primary mr-1"></i>'
    # elif rate < 1: 
    #     code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
    # else:
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'

    # if rate < 3/2: 
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'
    # elif rate < 2: 
    #     code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
    # else:
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'

    # if rate < 5/2: 
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'
    # elif rate < 3: 
    #     code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
    # else:
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'

    # if rate < 7/2: 
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'
    # elif rate < 4: 
    #     code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
    # else:
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'

    # if rate < 9/2: 
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'
    # elif rate < 5: 
    #     code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>'
    # else:
    #     code += '<i class="fas fa-star text-primary mr-1"></i>'

    for i in range(1, 6):
        if rate < (2*i-1) / 2: 
            code += '<i class="far fa-star text-primary mr-1"></i>\n'
        elif rate < i: 
            code += '<i class="fas fa-star-half-alt text-primary mr-1"></i>\n'
        else:
            code += '<i class="fas fa-star text-primary mr-1"></i>\n'
    return mark_safe(code)