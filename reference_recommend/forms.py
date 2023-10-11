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

    user_agent = ''

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
                    'placeholder': '해당 자료에 대해 간단히 설명해주세요',
                    'aria-describedby':'memoHelp'                    
                }
            )
        }
        

    # url 검증 
    def clean_url(self):
        url = self.cleaned_data['url']
        
        # 헤더 설정하지 않으면 크롤링 봇으로 인식하여 406 에러 발생하는 경우 있음
        headers = { 'User-Agent': self.user_agent }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValidationError('정확한 링크인지 확인해주세요. (response code: { %(status_code)s })',
                                  params={"status_code": response.status_code})
        else:           
            response.encoding = 'utf-8' # 한글이 깨지지 않도록 설정
            html = response.text            
            soup = BeautifulSoup(html, 'html.parser')
            
            # 사이트 제목
            title = soup.select_one('meta[property="og:title"]')
            
            if title:
                title = title['content']
                
                if len(title) > 17:
                    self.instance.title = title[:14] + '...'
                else:
                    self.instance.title = title
            else:    
                self.instance.title = ''
            
            
            # 사이트 썸네일
            image_url = soup.select_one('meta[property="og:image"]')
            
            if image_url:
                image_url = image_url['content']
            
                # 이미지 url이 상대경로로 적힌 경우 처리
                if image_url.startswith('/'):
                    _url = url.split('://')
                    top_url = _url[0] + '://' + _url[1].split('/')[0]
                    self.instance.image = top_url + image_url
                else:
                    self.instance.image = image_url

                
            # 사이트 설명    
            desc = soup.select_one('meta[property="og:description"]')
            
            if desc:
                desc = desc['content']
                
                if len(desc) > 40:
                    self.instance.description = desc[:37] + '...'
                else:
                    self.instance.description = desc
                    
            else:
                self.instance.description = ''

        return url
