from django.templatetags.static import register


@register.filter()
def my_media(data):
    if data:
        return f'/media/{data}'
    return '/media/no_content.webp'
