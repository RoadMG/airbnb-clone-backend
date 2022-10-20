from django.db import models


class CommonModel(models.Model):

    """Common Model Definition"""

    created = models.DateTimeField(
        auto_now_add=True,
    )
    """auto_now_add 는 필드의 값을 해당 object가 처음 생성되었을 때의 시간으로 설정 
    > room이 만들어지면 Django는 이 room이 만들어진 date를 이 부분에 넣는다는 뜻"""

    updated = models.DateTimeField(
        auto_now=True,
    )
    """auto_now 는 object가 저장될 때마다 해당 필드를 현재 date로 설정
    > room이 업데이트 할 때마다 저장"""

    class Meta:
        abstract = True

        """abstract : 데이터베이스에 올리지 않고 참조용으로만 사용한다"""
