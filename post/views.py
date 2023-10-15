from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .models import Post, Comment
from .forms import CustomPaginator, PostForm
from site4programmers.views import WriterMixin


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('post:post_list')
    form_class = PostForm

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)
    


class PostUpdateView(WriterMixin, UpdateView):
    model = Post
    template_name = 'post/post_create.html'
    success_url = reverse_lazy('post:post_detail')
    form_class = PostForm


    def get_success_url(self) -> str:
        return reverse('post:post_detail', kwargs={'pk':self.object.id})


class PostDeleteView(WriterMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post:post_list')



class PostListView(ListView):
    model = Post
    template_name = 'post/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-modify_dt']
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.custom_paginator = CustomPaginator(on_each_side = 4)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context.update(self.custom_paginator.get_pagination(page))

        return context


class MyPostListView(LoginRequiredMixin, ListView):
    template_name = 'post/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(writer=self.request.user).order_by('-modify_dt')
    

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        comments = self.object.comments.all()

        context = super().get_context_data(**kwargs)
        context['comments'] = comments        
        
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']
    success_url = reverse_lazy('post:post_list')

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse('post:post_detail', kwargs={'pk':self.object.post.id})


class CommentUpdateView(WriterMixin, UpdateView):
    model = Comment
    fields = ['content']
    success_url = reverse_lazy('post:post_detail')

    def get_success_url(self) -> str:
        return reverse('post:post_detail', kwargs={'pk':self.object.post.id})


class CommentDeleteView(WriterMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('post:post_detail')

    def get_success_url(self) -> str:
        return reverse('post:post_detail', kwargs={'pk':self.object.post.id})
