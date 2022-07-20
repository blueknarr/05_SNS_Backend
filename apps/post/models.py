from django.db import models
from user.models import User


# Create your models here.
class Post(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100, blank=True)
    content = models.TextField('본문')
    like = models.IntegerField('좋아요', default=0)
    view = models.IntegerField('조회수', default=0)
    create_date = models.DateTimeField('만든 날짜', auto_now_add=True)
    modify_date = models.DateTimeField('수정한 날짜', auto_now=True)

    class Meta:
        verbose_name = 'post'
        db_table = 'tb_post'
        ordering = ('-modify_date',)

    def __str__(self):
        return self.title
