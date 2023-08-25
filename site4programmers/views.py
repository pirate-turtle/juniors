from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin

from reference_recommend.models import ReferenceLink
from post.models import Post


class HomeView(TemplateView):
    template_name='home.html'


class UserJoinView(CreateView):
    template_name = 'registration/join.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('join_done')

    def form_valid(self, form):
        # 가입한 유저를 DB에 등록하기 위해 부모 함수 호출
        response = super().form_valid(form)

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)

        return response    
    

class UserJoinCompleteView(TemplateView):
    template_name = 'registration/join_done.html'


class WriterMixin(AccessMixin):
    raise_exception = False

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.writer:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
    

class MyPageView(LoginRequiredMixin, ListView):
    template_name = 'mypage.html'
    context_object_name = 'posts'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['links'] = ReferenceLink.objects.filter(writer=self.request.user).order_by('-id')        
        
        return context
    

    def get_queryset(self):
        return Post.objects.filter(writer=self.request.user).order_by('-modify_dt')
    

class MyPagePostDeleteView(WriterMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('mypage')


class MyPageLinkDeleteView(WriterMixin, DeleteView):
    model = ReferenceLink
    success_url = reverse_lazy('mypage')
    
        