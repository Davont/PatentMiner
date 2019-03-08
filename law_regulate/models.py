from django.db import models

# Create your models here.

"""
法律法规的数据库
"""


class LawRegulate(models.Model):
    law_id = models.CharField(max_length=10,null=True)              # 每个json文件里id标识
    category = models.CharField(max_length=100,null=True)           # 法律的类别
    law_title = models.CharField(max_length=150,null=True)          # 法律标题
    publish_time = models.CharField(max_length=20,null=True)        # 颁布时间
    effect_time = models.CharField(max_length=20,null=True)      # 生效时间
    content = models.TextField(null=True)                           # 法律内容
    json_tile = models.CharField(max_length=35,null=True)           # 所属的那个json文件名

    class Meta:
        db_table = 'regulate_info'
