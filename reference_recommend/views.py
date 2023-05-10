from typing import Any, Dict
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import ReferenceLink
from .forms import LinkRegisterForm
import requests
from bs4 import BeautifulSoup

# 추천한 링크 리스트 넘기기
class LinkListView(ListView):
    model = ReferenceLink    
    template_name = 'reference_recommend/link_list.html'


# 추천할 링크 리스트 등록하기
class LinkCreateView(CreateView):
    form_class = LinkRegisterForm
    success_url = reverse_lazy('recommend:link_list')
    template_name = 'reference_recommend/link_list_create.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = ReferenceLink.Category.choices
        return context

    ## TODO
    def form_valid(self, form):
        url = form.cleaned_data['url']
        print(url)
        print(form.instance)
        response = requests.get(url)

        if response.status_code == 200:
            response.encoding = "utf-8" # 한글이 깨지지 않도록 설정
            html = response.text            
            soup = BeautifulSoup(html, 'html.parser')
            form.instance.title = soup.select_one('meta[property="og:title"]')['content']

            image_url = soup.select_one('meta[property="og:image"]')['content']
            # 이미지 url이 상대경로로 적힌 경우 처리
            if image_url.startswith("/"):
                _url = url.split("://")
                top_url = _url[0] + "://" + _url[1].split("/")[0]
                form.instance.image = top_url + image_url
            else:
                form.instance.image = image_url

            # 사이트 설명이 30자를 초과하는 경우 처리
            desc = soup.select_one('meta[property="og:description"]')['content']
            if len(desc) > 30:
                form.instance.description = desc[:27] + '...'
            else:
                form.instance.description = desc

            
            
        else:
            ## TODO 오류 페이지로 연동
            print(response.status_code)

        return super().form_valid(form)
