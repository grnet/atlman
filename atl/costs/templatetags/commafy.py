from django import template

register = template.Library()

def commafy(value):
    if isinstance(value, basestring):
        return value.replace('.', ',')
    elif isinstance(value, float):
        return ('%f' % value).replace('.', ',')
    else:
        return value
    
commafy = register.filter(commafy)