#coding=UTF-8
from django.http import HttpResponse
from elasticsearch import Elasticsearch
import json
client = Elasticsearch(hosts=["127.0.0.1"])
from datetime import datetime
from . import base_search
from . import test_search
from .models import PatentInfo
from .models import PatentOtherInfo
from .models import LawStatus
from .models import Reference
from django.core import serializers
from django.shortcuts import render,HttpResponse
import ast
import xlwt
from datetime import time
# Create your views here.

def index(request):
    return render(request, 'sitesearch/index.html')

# 根据关键词到数据库中查询相关数据并返回结果界面
def word_search(request):
    try:
        # 获取普通搜索关键词
        key_words = request.GET.get('q', '')    # 获取到请求词
        page = request.GET.get('p', '1')        # 获取访问页码
        num = request.GET.get('n', '10')          # 获取每页显示数量
        order = request.GET.get('o', 'default')        # 获取排序方式
        f = request.GET.get('f', '0')                # 前台显示方式
        f_flag = request.GET.get('f_flag', '0')      # 高级搜索标志
        print("keywords"+key_words)
        print("f:"+f)

        # 获取高级搜索关键词
        final_words = {}
        appli_num = request.GET.get('appli_num', '')  # 申请号
        appli_time = request.GET.get('appli_time', '')  # 申请日
        patent_name = request.GET.get('patent_name', '')  # 名称
        pub_num = request.GET.get('pub_num', '')  # 公开号
        pub_time = request.GET.get('pub_time', '')  # 公开日
        # cpc_classifi = request.GET.get('cpc_classifi', '')  # cpc分类号
        ipc_classifi = request.GET.get('ipc_classifi', '')  # ipc分类号
        proposer = request.GET.get('proposer', '')  # 申请人
        inventor = request.GET.get('inventor', '')  # 发明人
        # angent = request.GET.get('angent', '')  # 代理人
        # angency = request.GET.get('angency', '')  # 代理机构
        # patent_type = request.GET.get('patent_type', '')  # 专利类型
        final_words["SQH"] = appli_num
        final_words["GKH"] = pub_num
        final_words["ZLMC"] = patent_name
        # final_words["CPC"] = cpc_classifi
        final_words["IPC"] = ipc_classifi
        final_words["SQR"] = proposer
        # final_words["DLR"] = angent
        final_words["SQSJ"] = appli_time
        final_words["GKSJ"] = pub_time
        final_words["FMR"] = inventor
        # final_words["DLJG"] = angency
        # final_words["ZLLX"] = patent_type
        print("final_words1"+str(final_words))

        if f_flag == '2':
            final_words = ast.literal_eval(key_words)
            print("fin_words2"+str(final_words))
        elif f_flag == '1':
            f_flag = '2'
            final_words["SSC"] = key_words


        # 结果筛选
        filter_words = {}
        key_words2 = request.GET.get('key_words2', '')      # 搜索条款关键词
        search_date = request.GET.get('search_date', '')        # 筛选条款日期
        begin_date = request.GET.get('begin_date', '')          # 开始日期
        end_date = request.GET.get('end_date', '')              # 结束日期
        language = request.GET.get('language', '')              # 专利语言
        # patent_type = request.GET.get('patent_type', '')        # 专利类型
        legal_status = request.GET.get('legal_status', '')      # 专利法律状态
        filter_words["SSC"] = key_words2
        filter_words["SSRQ"] = search_date
        filter_words["QSRQ"] = begin_date
        filter_words["JSRQ"] = end_date
        filter_words["ZLYY"] = language
        # filter_words["ZLLX"] = patent_type
        filter_words["FLZT"] = legal_status
        print(filter_words)

        fil_flag = '0'
        for m in filter_words:
            if filter_words[m]:
                fil_flag = '1'
        print("f_flag:"+str(f_flag))
        print("fil_flag:"+str(fil_flag))
        try:
            page = int(page)
        except:
            page = 1
        try:
            num = int(num)
        except:
            num = 10
        test = False
        if (not key_words) and (f_flag == '0'):     # 若搜索栏为空，返回主页
            return render(request, 'sitesearch/index.html')
        else:
            if test == True:
                search_result = test_search.main(key_words, page, num, order, final_words, filter_words, f_flag, fil_flag)
            else:
                search_result = base_search.main(key_words, page, num, order, final_words, filter_words, f_flag, fil_flag)
            return render(request, 'sitesearch/patent_list.html',
                          {"search_result": search_result["last_result"],       # 数据列表
                           "key_words": search_result["key_words"],             # 搜索关键词
                           "filter_words": filter_words,                         # 筛选词
                           "page": search_result["page"],                       # 当前页码
                           "total_nums": search_result["total_nums"],           # 数据总条数
                           "page_nums": search_result["page_nums"],             # 页数
                           "last_time": search_result["last_time"],             # 搜索时间
                           "front": search_result["front"],                     # 是否有上一页
                           "after": search_result["after"],                     # 是否有下一页
                           #"ssc": final_words["SSC"],                            # 高级搜索搜索词
                           "f": f,                                              # 前台显示方式
                           "o": order,
                           "n": num,                                            # 每页显示数量
                           "f_flag": f_flag,                                     # 高级搜索标志
                           "invcount_result": search_result["invcount"],        # 发明人统计结果
                           "ipccount_result": search_result["ipccount"],        # IPC分类号统计结果
                           "procount_result": search_result["procount"],        # 申请人统计结果

                           })                                                   # 显示页面和将列表和搜索词返回到html

    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

# 查看专利完整信息
def detail(request):
    try:
        print("detailstart")
        q = request.GET.get('q')
        print(q)
        patent_info_search = PatentInfo.objects.filter(patent_Id=q)
        patentotherinfo_search = PatentOtherInfo.objects.filter(patent_info=q)
        lawstatus_search = LawStatus.objects.filter(patent_info=q)
        reference_search = Reference.objects.filter(patent_info=q)
        patent_info_trans = json.loads(serializers.serialize("json", patent_info_search))
        patentotherinfo_trans = json.loads(serializers.serialize("json", patentotherinfo_search))
        lawstatus_trans = json.loads(serializers.serialize("json", lawstatus_search))
        reference_trans = json.loads(serializers.serialize("json", reference_search))
        for n in lawstatus_trans:
            m1 = n['fields']['law_effective_date']
            m2 = m1[0:4]+'.'+m1[4:6]+'.'+m1[6:]
            n['fields']['law_effective_date'] = m2
        # print(lawstatus_trans)
        print("detailend")
        return render(request, 'sitesearch/detail.html', {'patent_info': patent_info_trans,
                                                          'patentotherinfo': patentotherinfo_trans,
                                                          'lawstatus': lawstatus_trans,
                                                          'reference': reference_trans})
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

# 专利收藏
def collect(request):
    try:
        patent_id = request.POST.get('patent_id','')
        # 获取要放入购物车中的商品信息
        if patent_id:
            patent_search = PatentInfo.objects.get(patent_Id=patent_id)
            collect = patent_search.add()
            # 从session获取购物车信息，没有默认空字典
            collectlist = request.session.get('collectlist', {})
            # 判断此商品是否在购物车中
            if patent_id in collectlist:
                # 取消收藏
                del collectlist[patent_id]
            else:
                # 建立新收藏
                collectlist[patent_id] = collect
        else:
            collectlist = request.session.get('collectlist', {})
        # 将购物车信息放回到session
        request.session['collectlist'] = collectlist
        print(collectlist)
        return HttpResponse(json.dumps(collectlist))
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

# 获取收藏夹
def collection(request):
    try:
        collectlist = request.session.get('collectlist', {})
        print(collectlist)
        return render(request, "sitesearch/collection.html", locals())
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response
    return render(request, "sitesearch/collection.html")

# 导出Excel
def excel_export(request):
    try:
        patent_list = request.POST.getlist('patent_list')
        print("test")
        print(patent_list)
        # patent_list = ['CN201610482669.820180105FM','CN201610490172.020160914FM','CN201610505659.120180109FM',
        #                'CN201610539890.220161207FM','CN201610552692.X20161207FM','CN201610350337.420171201FM',
        #                'CN201610597401.920180202FM','CN201610388003.620171212FM']
        print(type(patent_list))
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=download.xls'
        
        workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
        sheet = workbook.add_sheet("sheet1")  # 创建工作页
        row0 = [u'专利名称', u'专利申请号', u'申请日期', u'公开号', u'公开日', u'申请人',
                u'发明人', u'申请人地址', u'IPC分类号', u'法律状态', u'优先权号', u'优先权日'
                ]
        alignment1 = xlwt.Alignment()
        alignment1.horz = xlwt.Alignment.HORZ_CENTER
        alignment1.vert = xlwt.Alignment.VERT_CENTER
        alignment1.wrap = xlwt.Alignment.WRAP_AT_RIGHT
        font1 = xlwt.Font()
        font1.name = "SimSun"
        font1.bold = True
        font1.height = 11 * 20
        style1 = xlwt.XFStyle()
        style1.alignment = alignment1
        style1.font = font1
        for i in range(0, len(row0)):
            sheet.write(0, i, row0[i], style1)
            sheet.col(i).width = 256 * 25
        num = 1
        font2 = xlwt.Font()
        font2.name = "SimSun"
        font2.height = 10 * 20
        style2 = xlwt.XFStyle()
        style2.alignment = alignment1
        style2.font = font2
        for n in patent_list:
            date_search = PatentInfo.objects.filter(patent_Id=n)
            date_trans = json.loads(serializers.serialize("json", date_search))
            sheet.write(num, 0, date_trans[0]['fields']['patent_name'], style2)
            sheet.write(num, 1, date_trans[0]['fields']['appli_num'], style2)
            sheet.write(num, 2, date_trans[0]['fields']['appli_time'], style2)
            sheet.write(num, 3, date_trans[0]['fields']['pub_num'], style2)
            sheet.write(num, 4, date_trans[0]['fields']['pub_time'], style2)
            sheet.write(num, 5, date_trans[0]['fields']['proposer'], style2)
            sheet.write(num, 6, date_trans[0]['fields']['inventor'], style2)
            sheet.write(num, 7, date_trans[0]['fields']['proposer_addr'], style2)
            sheet.write(num, 8, date_trans[0]['fields']['ipc_classifi'], style2)
            sheet.write(num, 9, date_trans[0]['fields']['legel_status'], style2)
            sheet.write(num, 10, date_trans[0]['fields']['priority_num'], style2)
            sheet.write(num, 11, date_trans[0]['fields']['priority_time'], style2)
            num = num + 1
        workbook.save(response)
        print('11111111111111111111111111111')
        return response
        
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response