# Generated by Django 4.0.6 on 2022-07-28 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'tag',
                'db_table': 'tb_tag',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False, null=True)),
                ('title', models.CharField(max_length=100, verbose_name='제목')),
                ('writer', models.CharField(max_length=20, verbose_name='작성자')),
                ('content', models.TextField(verbose_name='본문')),
                ('view', models.IntegerField(default=0, verbose_name='조회수')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='만든 날짜')),
                ('modify_date', models.DateTimeField(auto_now=True, verbose_name='수정한 날짜')),
                ('hashtag', models.ManyToManyField(related_name='HashTags', to='post.posttag')),
            ],
            options={
                'verbose_name': 'post',
                'db_table': 'tb_post',
                'ordering': ('-create_date',),
            },
        ),
    ]
