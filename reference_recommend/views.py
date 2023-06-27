from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ReferenceLink
from .forms import LinkRegisterForm
from site4programmers.views import WriterMixin


# 추천한 링크 리스트 넘기기
class LinkListView(ListView):
    model = ReferenceLink    
    template_name = 'reference_recommend/link_list.html'


# 추천할 링크 리스트 등록하기
class LinkCreateView(LoginRequiredMixin, CreateView):
    model = ReferenceLink
    form_class = LinkRegisterForm
    success_url = reverse_lazy('recommend:link_list')
    template_name = 'reference_recommend/link_list_create.html'       
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # user agent 추출해서 url 검증 단계에 헤더로 사용할 수 있도록 넘겨주기
        form = self.get_form_class()
        form.user_agent = self.request.META['HTTP_USER_AGENT']

        context = super().get_context_data(**kwargs)
        context['category'] = ReferenceLink.Category.choices                

        return context
    
    def form_valid(self, form):
        form.instance.writer = self.request.user

        return super().form_valid(form)


# 등록한 추천자료 링크 보기
class MyLinkListView(LoginRequiredMixin, ListView):
    template_name = 'reference_recommend/link_list.html'

    def get_queryset(self):
        return ReferenceLink.objects.filter(writer=self.request.user)


# 등록한 추천자료 링크 수정
class LinkUpdateView(WriterMixin, UpdateView):
    model = ReferenceLink
    form_class = LinkRegisterForm
    template_name = 'reference_recommend/link_list_create.html'
    success_url = reverse_lazy('recommend:link_list')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = ReferenceLink.Category.choices
        context['user_agent'] = self.request.META['HTTP_USER_AGENT']
        return context


# 등록한 추천자료 링크 삭제
class LinkDeleteView(WriterMixin, DeleteView):
    model = ReferenceLink
    success_url = reverse_lazy('recommend:link_list')