# 자동 생성되는 form 태그에 css 적용하기
# https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
# https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/#django.forms.ModelForm
from django.forms import ModelForm
from django.forms import TextInput
from django.core.exceptions import ValidationError
from .models import ReferenceLink
import requests

from bs4 import BeautifulSoup


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
        

    # url 검증 
    def clean_url(self):
        # TODO View에서 request header에서 user agent 추출까지는 성공
        # context 데이터 받아와서 requests 헤더로 설정해야함
        url = self.cleaned_data['url']
        response = requests.get(url)        

        if response.status_code != 200:
            raise ValidationError('정확한 링크인지 확인해주세요. (response code: { %(status_code)s })',
                                  params={"status_code": response.status_code})
        else:           
            response.encoding = 'utf-8' # 한글이 깨지지 않도록 설정
            html = response.text            
            soup = BeautifulSoup(html, 'html.parser')
            self.instance.title = soup.select_one('meta[property="og:title"]')['content']

            image_url = soup.select_one('meta[property="og:image"]')['content']
            # 이미지 url이 상대경로로 적힌 경우 처리
            if image_url.startswith('/'):
                _url = url.split('://')
                top_url = _url[0] + '://' + _url[1].split('/')[0]
                self.instance.image = top_url + image_url
            else:
                self.instance.image = image_url

            # 사이트 설명이 30자를 초과하는 경우 처리
            desc = soup.select_one('meta[property="og:description"]')['content']
            if len(desc) > 30:
                self.instance.description = desc[:27] + '...'
            else:
                self.instance.description = desc

        return url
