from django.db import models
from django.contrib.auth.models import User

# 추천하는 자료 링크
class ReferenceLink(models.Model):
    """
    사용자 입력
    - 필수
      - url : url    
      - 카테고리 (관련된 분야) : text, choices
      - 메모 : text 

    등록 이후 시스템에서 채우기
    - og tag 활용
      - 제목 : text
      - 설명 : text
      - 이미지 : image

    - 표시할 링크 (너무 길 경우를 대비해서 https://~/ 까지만 자르기)
    - 해당 자료를 등록한 유저의 username
    """
    
    url = models.URLField(max_length=200, unique=True)
    memo = models.CharField(max_length=50)
    
    class Category(models.TextChoices):        
        WEB = 'wb', 'Web'
        MOBILE = 'mb', 'Mobile'
        DATA = 'dt', 'Data'
        DB = 'db', 'Data Base'
        GAME = 'gm', 'Game'
        AI = 'ai', 'AI'
        CS = 'cs', 'CS'
        ETC = 'et', 'etc'    

    category = models.CharField(
        max_length=2,
        choices=Category.choices,
        default=Category.ETC
    )

    title = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=40, blank=True, null=True)
    image = models.URLField(max_length=200, blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)