from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # From mySpartaSns import settings 괜찮지만 장고가 관리하는 곳에서 장고보고 가져오게


# Create your models here.
class UserModel(AbstractUser):  # 장고의 기본 모델 AbstractUser에 우리거 추가할거얌
    class Meta:  # DB 테이블의 이름을 지정해주는 정보. 테이터베이스에 정보를 넣어준다.
        db_table = "my_user"  # 여기는 테이블 이름!! = 내 테이블 이름이 my_user 였으면 좋겠다.

    # 해당하는 곳, 각각의 정보들이 어떤 형태로 DB에 들어갈 것인지 설정. 장고 모델 필드의 종류 참조.
    bio = models.CharField(max_length=256, default='')
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followee')  # 사용자가 사용자를 (follow 안에는 사용자 정보가 들어간다)
