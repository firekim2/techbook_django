from django import template


register = template.Library()

def update_content(old_content, new_content):
    return new_content

register.filter('update_content', update_content)
