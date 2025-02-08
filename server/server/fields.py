from django.db import models
from django.forms import TextInput
from django.core.validators import RegexValidator

class ColorField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('validators', [RegexValidator(regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')])
        kwargs.setdefault('help_text', 'Valid Hexadecimal Color Code, ie. #0066ff. Use #000 for null')
        kwargs.setdefault('default', '#000000')
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        if value:
            # if '#000' in value:
            #     value = None
            if self.blank and self.null and '#000' in value:  # allows for nones in the widget
                value = None
        return super().clean(value, model_instance)

    def formfield(self, **kwargs):
        kwargs['widget'] = TextInput(attrs={'type': 'color'})
        return super().formfield(**kwargs)