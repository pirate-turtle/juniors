# 자동 생성되는 form 태그에 css 적용하기
# https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#django.forms.ModelForm
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import RadioSelect
from .models import ReferenceLink

class LinkRegisterForm(ModelForm):
    class Meta:
        model = ReferenceLink
        fields = ['url', 'memo', 'category']
        widgets = {
            'url': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'https://example.com',
                    'pattern': 'https://.*',
                    'aria-describedby':'urlHelp'
                    }
            ),

            'memo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '해당 자료에 대해 간단히 설명해주세요 (선택)',
                    'aria-describedby':'memoHelp'
                }
            )
        }
