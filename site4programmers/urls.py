from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from site4programmers.views import HomeView, UserJoinView, UserJoinCompleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/join/', UserJoinView.as_view(), name='join'),
    path('auth/join/done/', UserJoinCompleteView.as_view(), name='join_done'),
    path('', HomeView.as_view()),
    path('recommend/', include('reference_recommend.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# media 폴더에서 파일 읽어오기 위해 추가
# https://docs.djangoproject.com/en/3.2/howto/static-files/#serving-files-uploaded-by-a-user-during-development

# production 환경에서 별도의 파일 서버나 CDN을 통해 서비스하는 경우 적합하지 않은 방법임
# https://docs.djangoproject.com/en/3.2/howto/static-files/deployment/
