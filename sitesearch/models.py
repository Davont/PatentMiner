# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# 主信息表
class PatentInfo(models.Model):
    patent_Id = models.CharField(max_length=100,primary_key=True)           # 专利唯一标识(主键)
    patent_name = models.CharField(max_length=300)                          # 专利名称
    appli_num = models.CharField(max_length=50)                             # 申请号（唯一）
    appli_time = models.CharField(max_length=50,null=True)                  # 申请时间
    appli_num2 = models.CharField(max_length=50, null=True)                 # 去掉小数点的申请号（用来标识同族）
    pub_num = models.CharField(max_length=50)                               # 公开（公告）号
    pub_time = models.CharField(max_length=50,null=True)                    # 公开（公告）日期
    proposer = models.CharField(max_length=50, null=True)                   # 申请（专利权）人
    inventor = models.CharField(max_length=250, null=True)                  # 发明（设计）人
    proposer_addr = models.CharField(max_length=500, null=True)             # 申请人地址
    ipc_classifi = models.CharField(max_length=2000, null=True)             # IPC分类号
    patent_abs = models.TextField(null=True)                                # 摘要内容
    lang = models.CharField(max_length=30, null=True)                       # 所属语言
    legel_status = models.CharField(max_length=1000, null=True)             # 法律状态
    priority_num = models.CharField(max_length=1000, null=True)             # 优先权号
    priority_time = models.CharField(max_length=100,null=True)              # 优先权日

    class Meta:
        db_table = 'patent_info'                                            # 给表起的别名，数据库中显示的是该名字

    def add(self):
        return {'patent_Id':self.patent_Id, 'patent_name':self.patent_name, 'appli_num':self.appli_num,
                'appli_time':self.appli_time, 'pub_num ':self.pub_num , 'pub_time':self.pub_time,
                'proposer':self.proposer,'inventor':self.inventor,'proposer_addr':self.proposer_addr,
                'ipc_classifi':self.ipc_classifi,'legel_status':self.legel_status}

# 详细信息表
class PatentOtherInfo(models.Model):
    appli_num = models.CharField(max_length=50)                             # 申请号
    locarno_class = models.CharField(max_length=100, null=True)             # 洛迦诺分类
    intl_appli_data = models.CharField(max_length=100, null=True)           # 国际申请
    intl_pub_time = models.CharField(max_length=50, null=True)              # 国际公布
    entry_state_date = models.CharField(max_length=100,null=True)           # 进入国家日期
    keyword = models.CharField(max_length=1000, null=True)                  # 关键词
    cpc_classifi = models.CharField(max_length=2000, null=True)             # CPC分类号
    proposer_code = models.CharField(max_length=50,null=True)               # 申请人邮编
    angency = models.CharField(max_length=1000, null=True)                  # 代理机构
    angent = models.CharField(max_length=200, null=True)                    # 代理人
    patent_claims = models.TextField(null= True)                            # 权利要求书
    instructions = models.TextField(null=True)                              # 说明书
    abstract_image_path = models.TextField(max_length=700, null=True)       # 说明书附图路径
    patent_text_path = models.CharField(max_length=700, null=True)          # PDF文本路径
    law_time = models.CharField(max_length=100,null=True)                   # 法律最后生效时间
    patent_info = models.OneToOneField(PatentInfo,on_delete=models.CASCADE) # 和主信息建立一对一的关系

    class Meta:
        db_table = 'second_info'


# 法律状态表
class LawStatus(models.Model):
    law_effective_date = models.CharField(max_length=50,null=True)            # 法律状态生效日
    law_meaning = models.CharField(max_length=300,null=True)                  # 法律状态含义
    patent_info = models.ForeignKey(PatentInfo,on_delete=models.CASCADE)      # 和主信息建立一对多的关系（即一个专利对应多个法律状态）

    class Meta:
        db_table = 'law_info'


# 相关性表
class Reference(models.Model):
    id = models.AutoField(primary_key=True)                                     # 主键自动增加
    appli_num = models.CharField(max_length=50)                                 # 公开号（唯一）
    other_appli_num = models.CharField(max_length=50,null=True)                 # 相关专利的申请号
    other_pub_num = models.CharField(max_length=50,null=True)                   # 其他相关专利的公开号
    other_title = models.CharField(max_length=200,null=True)                    # 其他专利的名字
    correlate = models.CharField(max_length=20,null=True)                       # 专利之间关系（引证，被引，同族）
    patent_info = models.ForeignKey(PatentInfo,on_delete=models.CASCADE)        # 和主表建立一对多的关系

    class Meta:
        db_table = 'relate_info'









