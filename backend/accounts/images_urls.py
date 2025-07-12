from django.utils.text import slugify


def get_profile(instance, filename):
    safe_instance = slugify(instance)
    path = f'userprofile/image/{safe_instance}'
    safe_filename = slugify(filename)
    return f'{path}/{safe_filename}.webp'


