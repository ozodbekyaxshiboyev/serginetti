from django.core.exceptions import ValidationError


def location_image(instance, file):
    return f'users/{instance.role}/{instance.first_name}_{file}'

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

def custom_validator(value):
    valid_formats = ['png', 'jpeg', 'jpg', 'vsg']
    if not any([True if value.name.lower().endswith(i) else False for i in valid_formats]):
        raise ValidationError(f'{value.name} is not a valid image format')