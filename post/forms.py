from typing import Dict, Any
from django.core.paginator import Page
from django.forms import ModelForm
from django.forms import TextInput, Textarea
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post

        fields = ['title', 'content']
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '제목을 입력해주세요 (최대 50자)',
                    'style': 'width: 50%',
                    'aria-describedby':'titleHelp'
                    }
            ),

            'content': Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': '게시글 내용을 입력해주세요',
                    'style': 'width: 50%; resize: none; height: 500px',
                    'aria-describedby':'contentHelp'                    
                }
            )
        }



class CustomPaginator():
    def __init__(self, on_each_side=3):
        self.on_each_side = on_each_side

    def get_pagination(self, page: Page) -> Dict[str, Any]:
        pagination = {}

        start = max(1, page.number - self.on_each_side)
        end = min(start + self.on_each_side * 2, page.paginator.num_pages)
        pagination['page_range'] = range(start, end+1)

        pagination['has_prev_window'] = True
        if page.number > self.on_each_side + 1:
            pagination['prev_window_index'] = max(1, page.number - self.on_each_side * 2 - 1)
        else:
            pagination['has_prev_window'] = False


        pagination['has_next_window'] = True
        if page.number < page.paginator.num_pages - self.on_each_side:            
            pagination['next_window_index'] = min(page.number + self.on_each_side * 2 + 1, page.paginator.num_pages)
        else:
            pagination['has_next_window'] = False

        
        return pagination
