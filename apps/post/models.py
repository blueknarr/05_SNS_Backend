from django.db import models
from user.models import User


class SoftDeleteManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedRecordManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(null=True, default=False)

    class Meta:
        abstract = True

    objects = SoftDeleteManager()
    deleted_objects = DeletedRecordManager()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    def restore(self):
        self.is_deleted = False
        self.save(update_fields=["is_deleted"])


class Post(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('제목', max_length=100, null=False)
    writer = models.CharField('작성자', max_length=20, null=False)
    content = models.TextField('본문', null=False)
    hashtag = models.ManyToManyField('PostTag', related_name ='HashTags')
    like_users = models.ManyToManyField('PostLike', related_name ='Like')
    view = models.IntegerField('조회수', default=0)
    create_date = models.DateTimeField('만든 날짜', auto_now_add=True)
    modify_date = models.DateTimeField('수정한 날짜', auto_now=True)

    class Meta:
        verbose_name = 'post'
        db_table = 'tb_post'
        ordering = ('-create_date',)

    def __str__(self):
        return self.title


class PostTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.IntegerField('user_id')