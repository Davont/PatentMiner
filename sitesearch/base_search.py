#coding=UTF-8
from elasticsearch import Elasticsearch
from django.shortcuts import render
client = Elasticsearch(hosts=["127.0.0.1"])
from django.http import HttpResponse
import datetime
import re
import json


def main(key_words, page, num,order, final_words, filter_words, f_flag, fil_flag):
    try:
        print('start')
        key_words = key_words           # 获取到请求词
        page = page                     # 获取访问页码
        num = num                       # 获取每页显示数量
        order = order                   # 获取排序方式
        final_words = final_words       # 获取高级搜索关键词
        filter_words = filter_words     # 获取结果筛选关键词
        start_time = datetime.datetime.now()     # 获取搜索开始时间
        search_result = {}
        print(key_words)
        print(final_words)

        if f_flag == '0':
            final_word = key_words
            if fil_flag == '1':
                print("comonfilter")
                response = comfilter_search(key_words, page, num, order, filter_words)
            else:
                print("common")
                response = common_search(key_words, page, num, order)
        else:
            final_word = repr(final_words)
            if fil_flag == '1':
                print("multifilter")
                response = mulfilter_search(key_words,final_words, page, num, order, filter_words)
            else:
                print("multi")
                response = multi_search(final_words, page, num, order)

        end_time = datetime.datetime.now()  # 获取搜索结束时间
        last_time = (end_time - start_time).total_seconds()  # 计算搜索用时，转换成秒
        total_nums = response["hits"]["total"]  # 获取查询结果总条数
        if (page % num) > 0:  # 计算页数
            page_nums = int(total_nums / num) + 1
        else:
            page_nums = int(total_nums / num)
        if page == 1:  # 判断是否有上一页
            front = False
        else:
            front = True
        if page >= page_nums:  # 判断是否有下一页
            after = False
        else:
            after = True
        last_result = []  # 设置一个列表来储存搜索到的信息，返回给html页面
        for result in response["hits"]["hits"]:  # 循环查询到的结果
            result_dict = {}  # 设置一个字典来储存循环结果
            if "highlight" in result.keys():  # 判断是否有高亮字段
                if "patent_name.another" in result["highlight"]:  # 判断patent_name字段，如果高亮字段有类容
                    result_dict["patent_name"] = "".join(result["highlight"]["patent_name.another"])  # 获取高亮里的patent_name
                else:
                    result_dict["patent_name"] = result["_source"]["patent_name"]  # # 否则获取不是高亮里的patent_name

                result_dict["appli_num"] = result["_source"]["appli_num"]  # 申请号（唯一）
                result_dict["appli_time"] = result["_source"]["appli_time"]  # 申请时间
                result_dict["pub_time"] = result["_source"]["pub_time"]  # 公开时间
                if "proposer" in result["highlight"]:
                    result_dict["proposer"] = "".join(result["highlight"]["proposer"])
                else:
                    result_dict["proposer"] = result["_source"]["proposer"]  # 申请（专利权）人
                if "proposer_addr.another" in result["highlight"]:
                    result_dict["proposer_addr"] = "".join(result["highlight"]["proposer_addr.another"])
                else:
                    result_dict["proposer_addr"] = result["_source"]["proposer_addr"]  # 申请人地址
                if "inventor" in result["highlight"]:
                    result_dict["inventor"] = "".join(result["highlight"]["inventor"])
                else:
                    result_dict["inventor"] = result["_source"]["inventor"]  # 发明（设计）人
                if "patent_abs.another" in result["highlight"]:
                    result_dict["patent_abs"] = "".join(result["highlight"]["patent_abs.another"])
                else:
                    result_dict["patent_abs"] = result["_source"]["patent_abs"]  # 摘要内容
                result_dict["legel_status"] = result["_source"]["legel_status"]  # 法律状态
                result_dict["patent_id"] = result["_source"]["patent_id"]        # 专利id
                result_dict["ipc_classifi"] = result["_source"]["ipc_classifi"]        # ipc分类号
            else:
                result_dict["patent_name"] = result["_source"]["patent_name"]  # 专利名称
                result_dict["appli_num"] = result["_source"]["appli_num"]  # 申请号（唯一）
                result_dict["appli_time"] = result["_source"]["appli_time"]  # 申请时间
                result_dict["pub_time"] = result["_source"]["pub_time"]  # 公开时间
                result_dict["proposer"] = result["_source"]["proposer"]  # 申请（专利权）人
                result_dict["proposer_addr"] = result["_source"]["proposer_addr"]  # 申请人地址
                result_dict["inventor"] = result["_source"]["inventor"]  # 发明（设计）人
                result_dict["patent_abs"] = result["_source"]["patent_abs"]  # 摘要内容
                result_dict["legel_status"] = result["_source"]["legel_status"]  # 法律状态
                result_dict["patent_id"] = result["_source"]["patent_id"]        # 专利id
                result_dict["ipc_classifi"] = result["_source"]["ipc_classifi"]        # ipc分类号
            last_result.append(result_dict)
        invcount_result = []
        ipccount_result = []
        procount_result = []
        for inv in response["aggregations"]["inv"]["buckets"]:
            inv_dict = {}  # 设置一个字典来储存循环结果
            inv_dict["inventer"] = inv["key"]
            inv_dict["count"] = inv["doc_count"]
            a = inv["doc_count"]/total_nums
            inv_dict["percentage"] = '%.2f%%' % (a * 100)
            invcount_result.append(inv_dict)

        for ipc in response["aggregations"]["ipc"]["buckets"]:
            ipc_dict = {}  # 设置一个字典来储存循环结果
            ipc_dict["ipc"] = ipc["key"]
            ipc_dict["count"] = ipc["doc_count"]
            b = ipc["doc_count"]/total_nums
            ipc_dict["percentage"] = '%.2f%%' % (b * 100)
            ipccount_result.append(ipc_dict)

        for pro in response["aggregations"]["pro"]["buckets"]:
            pro_dict = {}  # 设置一个字典来储存循环结果
            pro_dict["proposer"] = pro["key"]
            pro_dict["count"] = pro["doc_count"]
            c = pro["doc_count"]/total_nums
            pro_dict["percentage"] = '%.2f%%' % (c * 100)
            procount_result.append(pro_dict)

        search_result["last_result"] = last_result
        search_result["key_words"] = final_word
        search_result["page"] = page
        search_result["total_nums"] = total_nums
        search_result["page_nums"] = page_nums
        search_result["last_time"] = last_time
        search_result["front"] = front
        search_result["after"] = after
        search_result["invcount"] = invcount_result
        search_result["ipccount"] = ipccount_result
        search_result["procount"] = procount_result

        print('end')
        return search_result
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

# 高级搜索
def multi_search(final_words, page, num, order):
    try:
        match = 0
        for n in final_words:
            if final_words[n] != "":
                match = match + 1
        if order == "appli_desc":   # 申请日降序
            response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                index="patent",  # 设置索引名称
                doc_type="doc",  # 设置表名称
                body={  # 书写elasticsearch语句
                    "query": {
                        "bool": {
                            "should": [
                                {"multi_match": {  # multi_match查询
                                    "query": final_words["SSC"],  # 查询关键词
                                    "fields": ["patent_name.another",  # 专利名称
                                               "proposer",  # 申请（专利权）人
                                               "proposer_addr.another",  # 申请人地址
                                               "inventor",  # 发明（设计）人
                                               # "cpc_classifi",  # CPC分类号
                                               "ipc_classifi",  # IPC分类号
                                               "priority_num.keyword",  # 优先权号
                                               "priority_time.another",  # 优先权日
                                               "patent_abs.another",  # 摘要内容
                                               ]  # 查询字段
                                }},
                                {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                # {"term": {"cpc_classifi.keyword": final_words["CPC]}},       # CPC分类号
                                {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                            ],
                            "minimum_should_match": match
                        }
                    },
                    "sort": [{
                        "appli_time.keyword": {
                            "order": "desc"
                        }
                    }],
                    "highlight": {
                        "require_field_match": False,
                        "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                        "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                    },
                    "aggs": {
                         "inv": {
                           "terms": {
                             "field": "inventor",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                         "ipc": {
                           "terms": {
                             "field": "ipc_classifi",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                          "pro": {
                           "terms": {
                             "field": "proposer",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         }
                    },
                    "from": (page - 1) * num,  # 从第几条开始获取
                    "size": num,  # 获取多少条数据
                }
            )
            return response
        elif order == "appli_asc":  # 申请日升序
            response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                index="patent",  # 设置索引名称
                doc_type="doc",  # 设置表名称
                body={  # 书写elasticsearch语句
                    "query": {
                        "bool": {
                            "should": [
                                {"multi_match": {  # multi_match查询
                                    "query": final_words["SSC"],  # 查询关键词
                                    "fields": ["patent_name.another",  # 专利名称
                                               "proposer",  # 申请（专利权）人
                                               "proposer_addr.another",  # 申请人地址
                                               "inventor",  # 发明（设计）人
                                               # "cpc_classifi",  # CPC分类号
                                               "ipc_classifi",  # IPC分类号
                                               "priority_num.keyword",  # 优先权号
                                               "priority_time.another",  # 优先权日
                                               "patent_abs.another",  # 摘要内容
                                               ]  # 查询字段
                                }},
                                {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                # {"term": {"cpc_classifi.keyword": final_words["CPC]}},       # CPC分类号
                                {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                            ],
                            "minimum_should_match": match
                        }
                    },
                    "sort": [{
                        "appli_time.keyword": {
                            "order": "asc"
                        }
                    }],
                    "highlight": {
                        "require_field_match": False,
                        "fields": {
                            "patent_name.another": {},
                            "appli_num.keyword": {},
                            "appli_time.keyword": {},
                            "proposer": {},
                            "proposer_addr.another": {},
                            "inventor": {},
                            "patent_abs.another": {"number_of_fragments": 0}
                        },
                        "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                    },
                    "aggs": {
                         "inv": {
                           "terms": {
                             "field": "inventor",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                         "ipc": {
                           "terms": {
                             "field": "ipc_classifi",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                          "pro": {
                           "terms": {
                             "field": "proposer",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         }
                    },
                    "from": (page - 1) * num,  # 从第几条开始获取
                    "size": num,  # 获取多少条数据
                }
            )
            return response
        elif order == "pub_desc":  # 公开日降序
            response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                index="patent",  # 设置索引名称
                doc_type="doc",  # 设置表名称
                body={  # 书写elasticsearch语句
                    "query": {
                        "bool": {
                            "should": [
                                {"multi_match": {  # multi_match查询
                                    "query": final_words["SSC"],  # 查询关键词
                                    "fields": ["patent_name.another",  # 专利名称
                                               "proposer",  # 申请（专利权）人
                                               "proposer_addr.another",  # 申请人地址
                                               "inventor.another",  # 发明（设计）人
                                               # "cpc_classifi",  # CPC分类号
                                               "ipc_classifi",  # IPC分类号
                                               "priority_num.keyword",  # 优先权号
                                               "priority_time.another",  # 优先权日
                                               "patent_abs.another",  # 摘要内容
                                               ]  # 查询字段
                                }},
                                {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                # {"term": {"cpc_classifi.keyword": final_words["CPC]}},       # CPC分类号
                                {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                            ],
                            "minimum_should_match": match
                        }
                    },
                    "sort": [{
                        "pub_time.keyword": {
                            "order": "desc"
                        }
                    }],
                    "highlight": {
                        "require_field_match": False,
                        "fields": {
                            "patent_name.another": {},
                            "appli_num.keyword": {},
                            "appli_time.keyword": {},
                            "proposer": {},
                            "proposer_addr.another": {},
                            "inventor": {},
                            "patent_abs.another": {"number_of_fragments": 0}
                        },
                        "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                    },
                    "aggs": {
                         "inv": {
                           "terms": {
                             "field": "inventor",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                         "ipc": {
                           "terms": {
                             "field": "ipc_classifi",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                          "pro": {
                           "terms": {
                             "field": "proposer",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         }
                    },
                    "from": (page - 1) * num,  # 从第几条开始获取
                    "size": num,  # 获取多少条数据
                }
            )
            return response
        elif order == "pub_asc":  # 公开日升序
            response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                index="patent",  # 设置索引名称
                doc_type="doc",  # 设置表名称
                body={  # 书写elasticsearch语句
                    "query": {
                        "bool": {
                            "should": [
                                {"multi_match": {  # multi_match查询
                                    "query": final_words["SSC"],  # 查询关键词
                                    "fields": ["patent_name.another",  # 专利名称
                                               "proposer",  # 申请（专利权）人
                                               "proposer_addr.another",  # 申请人地址
                                               "inventor",  # 发明（设计）人
                                               # "cpc_classifi",  # CPC分类号
                                               "ipc_classifi",  # IPC分类号
                                               "priority_num.keyword",  # 优先权号
                                               "priority_time.another",  # 优先权日
                                               "patent_abs.another",  # 摘要内容
                                               ]  # 查询字段
                                }},
                                {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                # {"term": {"cpc_classifi.keyword": final_words["CPC]}},       # CPC分类号
                                {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                            ],
                            "minimum_should_match": match
                        }
                    },
                    "sort": [{
                        "pub_time.keyword": {
                            "order": "asc"
                        }
                    }],
                    "highlight": {
                        "require_field_match": False,
                        "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                        "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                    },
                    "aggs": {
                         "inv": {
                           "terms": {
                             "field": "inventor",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                         "ipc": {
                           "terms": {
                             "field": "ipc_classifi",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                          "pro": {
                           "terms": {
                             "field": "proposer",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         }
                    },
                    "from": (page - 1) * num,  # 从第几条开始获取
                    "size": num,  # 获取多少条数据
                }
            )
            return response
        else:                   # 智能排序
            response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                index="patent",  # 设置索引名称
                doc_type="doc",  # 设置表名称
                body={  # 书写elasticsearch语句
                    "query": {
                        "bool": {
                            "should": [
                                {"multi_match": {  # multi_match查询
                                    "query": final_words["SSC"],  # 查询关键词
                                    "fields": ["patent_name.another",  # 专利名称
                                               "proposer",  # 申请（专利权）人
                                               "proposer_addr.another",  # 申请人地址
                                               "inventor",  # 发明（设计）人
                                               # "cpc_classifi",  # CPC分类号
                                               "ipc_classifi",  # IPC分类号
                                               "priority_num.keyword",  # 优先权号
                                               "priority_time.another",  # 优先权日
                                               "patent_abs.another",  # 摘要内容
                                               ]  # 查询字段
                                }},
                                {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                # {"term": {"cpc_classifi.keyword": final_words["CPC]}},       # CPC分类号
                                {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                            ],
                            "minimum_should_match": match
                        }
                    },
                    "highlight": {
                        "require_field_match": False,
                        "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                        "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                        "post_tags": ['</span>'],  # 高亮结束标签
                    },
                    "aggs": {
                         "inv": {
                           "terms": {
                             "field": "inventor",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                         "ipc": {
                           "terms": {
                             "field": "ipc_classifi",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         },
                          "pro": {
                           "terms": {
                             "field": "proposer",
                             "size": 10,
                             "order": {"_count": "desc"}
                           }
                         }
                    },
                    "from": (page - 1) * num,  # 从第几条开始获取
                    "size": num,  # 获取多少条数据
                }
            )
            return response
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

def common_search(key_words, page, num, order):
    try:
        if order == "appli_desc":  # 申请日降序
            if key_words.startswith("CN" or "US" or "WO" or "EP" or "PCT" or "TW"):  # 专利号搜索
                key_words = key_words.replace(' ', '')
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "multi_match": {  # multi_match查询
                                "query": key_words,  # 查询关键词
                                "fields": ["appli_num.keyword",  # 申请号（唯一）
                                           "pub_num.keyword",  # 公开（公告）号(唯一)
                                           "priority_num.keyword",  # 优先权号(唯一)
                                           ]  # 查询字段
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            elif re.search(r'\d{4}-\d{1,2}-\d{1,2}', key_words):  # 优先权申请/公开日查询
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"term": {"appli_time.keyword": key_words}},  # 申请日
                                    {"term": {"pub_time.keyword": key_words}},  # 公开日
                                    {"term": {"priority_time.keyword": key_words}},  # 公开日
                                ]
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [{  # should查询为满足一个或多个都匹配
                                    "multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   "ipc_classifi",  # IPC分类号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                ]
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],

                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
            return response
        elif order == "appli_asc":  # 申请日升序
            if key_words.startswith("CN" or "US" or "WO" or "EP" or "PCT" or "TW"):  # 专利号搜索
                key_words = key_words.replace(' ', '')
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "multi_match": {  # multi_match查询
                                "query": key_words,  # 查询关键词
                                "fields": ["appli_num.keyword",  # 申请号（唯一）
                                           "pub_num.keyword",  # 公开（公告）号(唯一)
                                           "priority_num.keyword",  # 优先权号(唯一)
                                           ]  # 查询字段
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            elif re.search(r'\d{4}-\d{1,2}-\d{1,2}', key_words):  # 申请/公开日查询
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"term": {"appli_time.keyword": key_words}},  # 申请日
                                    {"term": {"pub_time.keyword": key_words}},  # 公开日
                                    {"term": {"priority_time.keyword": key_words}},  # 公开日
                                ]
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [{  # should查询为满足一个或多个都匹配
                                    "multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   "ipc_classifi",  # IPC分类号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                ]
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
            return response
        elif order == "pub_desc":  # 公开日降序
            if key_words.startswith("CN" or "US" or "WO" or "EP" or "PCT" or "TW"):  # 专利号搜索
                key_words = key_words.replace(' ', '')
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "multi_match": {  # multi_match查询
                                "query": key_words,  # 查询关键词
                                "fields": ["appli_num.keyword",  # 申请号（唯一）
                                           "pub_num.keyword",  # 公开（公告）号(唯一)
                                           "priority_num.keyword",  # 优先权号(唯一)
                                           ]  # 查询字段
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            elif re.search(r'\d{4}-\d{1,2}-\d{1,2}', key_words):  # 申请/公开日查询
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"term": {"appli_time.keyword": key_words}},  # 申请日
                                    {"term": {"pub_time.keyword": key_words}},  # 公开日
                                    {"term": {"priority_time.keyword": key_words}},  # 优先权日
                                ]
                            }
                        },
                        "sort": [{
                            "pub_time.keywford": {
                                "order": "desc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [{  # should查询为满足一个或多个都匹配
                                    "multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   "ipc_classifi",  # IPC分类号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                ]
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                              "patent_name.another": {},
                              "appli_num.keyword": {},
                              "appli_time.keyword": {},
                              "proposer": {},
                              "proposer_addr.another": {},
                              "inventor": {},
                              "patent_abs.another": {"number_of_fragments": 0}
                        },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
            return response
        elif order == "pub_asc":  # 公开日升序
            if key_words.startswith("CN" or "US" or "WO" or "EP" or "PCT" or "TW"):  # 专利号搜索
                key_words = key_words.replace(' ', '')
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "multi_match": {  # multi_match查询
                                "query": key_words,  # 查询关键词
                                "fields": ["appli_num.keyword",  # 申请号（唯一）
                                           "pub_num.keyword",  # 公开（公告）号(唯一)
                                           "priority_num.keyword",  # 优先权号(唯一)
                                           ]  # 查询字段
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            elif re.search(r'\d{4}-\d{1,2}-\d{1,2}', key_words):  # 申请/公开日查询
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"term": {"appli_time.keyword": key_words}},  # 申请日
                                    {"term": {"pub_time.keyword": key_words}},  # 公开日
                                    {"term": {"priority_time.keyword": key_words}},  # 公开日
                                ]
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [{  # should查询为满足一个或多个都匹配
                                    "multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   "ipc_classifi",  # IPC分类号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                ]
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
            return response
        else:                     # 智能排序
            if key_words.startswith("CN" or "US" or "WO" or "EP" or "PCT" or "TW"):  # 专利号搜索
                key_words = key_words.replace(' ', '')
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "multi_match": {  # multi_match查询
                                "query": key_words,  # 查询关键词
                                "fields": ["appli_num.keyword",  # 申请号（唯一）
                                           "pub_num.keyword",  # 公开（公告）号(唯一)
                                           "priority_num.keyword",  # 优先权号(唯一)
                                           ]  # 查询字段
                            }
                        },
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            elif re.search(r'\d{4}.\d{1,2}.\d{1,2}', key_words):  # 申请/公开日查询
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"term": {"appli_time.keyword": key_words}},  # 申请日
                                    {"term": {"pub_time.keyword": key_words}},  # 公开日
                                    {"term": {"priority_time.keyword": key_words}},  # 优先权日
                                ]
                            }
                        },
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num  # 获取多少条数据
                    }
                )
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [{  # should查询为满足一个或多个都匹配
                                    "multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   "ipc_classifi",  # IPC分类号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                ]
                            }
                        },
                         "aggs": {
                             "inv": {
                               "terms": {
                                 "field": "inventor",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                             "ipc": {
                               "terms": {
                                 "field": "ipc_classifi",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             },
                              "pro": {
                               "terms": {
                                 "field": "proposer",
                                 "size": 10,
                                 "order": {"_count": "desc"}
                               }
                             }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": "false",  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
            return response
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

def comfilter_search(key_words, page, num, order, filter_words):
    try:
        key_words2 = filter_words["SSC"]
        key_words = str(key_words + key_words2)
        search_date = filter_words["SSRQ"]
        begin_date = filter_words["QSRQ"].replace("-", ".")
        end_date = filter_words["JSRQ"].replace("-", ".")
        language = filter_words["ZLYY"]
        legal_status = filter_words["FLZT"]

        match = 0
        for n in filter_words:
            if filter_words[n] != "":
                match = match+1

        if search_date:
            match = match - 1
            if begin_date == "":
                begin_date = "1800.01.01"
            else:
                match = match-1
            if end_date == "":
                end_date = "2200.12.31"
            else:
                match = match - 1
        if not key_words2:
            match = match+1

        if order == "appli_desc":  # 申请日降序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match":{"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                "patent_name.another": {},
                                "appli_num.keyword": {},
                                "appli_time.keyword": {},
                                "proposer": {},
                                "proposer_addr.another": {},
                                "inventor": {},
                                "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "appli_asc":  # 申请日升序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "pub_desc":  # 公开日降序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "pub_asc":  # 公开日升序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        else:
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [     # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {  # bool组合查询
                                "should": [  # should查询为满足一个或多个都匹配
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "highlight": {  # 高亮显示查询关键字
                            "require_field_match": False,  # 高亮显示所有字段
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

def mulfilter_search(key_words,final_words, page, num, order, filter_words):
    try:
        key_words2 = filter_words["SSC"]
        key_words = str(final_words["SSC"] + key_words2)
        search_date = filter_words["SSRQ"]
        begin_date = filter_words["QSRQ"].replace("-", ".")
        end_date = filter_words["JSRQ"].replace("-", ".")
        language = filter_words["ZLYY"]
        legal_status = filter_words["FLZT"]

        match = 0
        for n in final_words:
            if final_words[n] != "":
                match = match + 1
        for m in filter_words:
            if filter_words[m] != "":
                match = match + 1
        if key_words2 and final_words["SSC"]:
            match = match - 1

        if search_date:
            match = match - 1
            if begin_date == "":
                begin_date = "1800.01.01"
            else:
                match = match-1
            if end_date == "":
                end_date = "2200.12.31"
            else:
                match = match - 1

        if order == "appli_desc":   # 申请日降序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "appli_asc":  # 申请日升序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                "patent_name.another": {},
                                "appli_num.keyword": {},
                                "appli_time.keyword": {},
                                "proposer": {},
                                "proposer_addr.another": {},
                                "inventor": {},
                                "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "pub_desc":  # 公开日降序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                 "should": [
                                     {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                     {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                     {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                     {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                     {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                     # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                     {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                     {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                     {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                     # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                     # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                     # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                     {"multi_match": {  # multi_match查询
                                         "query": key_words,  # 查询关键词
                                         "fields": ["patent_name.another",  # 专利名称
                                                    "proposer",  # 申请（专利权）人
                                                    "proposer_addr.another",  # 申请人地址
                                                    "inventor",  # 发明（设计）人
                                                    # "cpc_classifi",  # CPC分类号
                                                    "ipc_classifi",  # IPC分类号
                                                    "priority_num.keyword",  # 优先权号
                                                    "priority_time.keyword",  # 优先权日
                                                    "patent_abs.another",  # 摘要内容
                                                    ]  # 查询字段
                                     }},
                                     {"match": {"lang.keyword": language}},
                                     {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "desc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        elif order == "pub_asc":  # 公开日升序
            if search_date == "pub_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "sort": [{
                            "appli_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",  # 设置索引名称
                    doc_type="doc",  # 设置表名称
                    body={  # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "sort": [{
                            "pub_time.keyword": {
                                "order": "asc"
                            }
                        }],
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1) * num,  # 从第几条开始获取
                        "size": num,  # 获取多少条数据
                    }
                )
                return response
        else:                   # 智能排序
            if search_date == "pub_time":
                response = client.search(               # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",                     # 设置索引名称
                    doc_type="doc",                     # 设置表名称
                    body={                              # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "pub_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1)*num,          # 从第几条开始获取
                        "size": num,                     # 获取多少条数据
                    }
                )
                return response
            elif search_date == "appli_time":
                response = client.search(               # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",                     # 设置索引名称
                    doc_type="doc",                     # 设置表名称
                    body={                              # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match,
                                "filter": {
                                    "range": {
                                        "appli_time": {
                                            "gte": begin_date,
                                            "lte": end_date
                                        }
                                    }
                                }
                            }
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1)*num,          # 从第几条开始获取
                        "size": num,                     # 获取多少条数据
                    }
                )
                return response
            else:
                response = client.search(               # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
                    index="patent",                     # 设置索引名称
                    doc_type="doc",                     # 设置表名称
                    body={                              # 书写elasticsearch语句
                        "query": {
                            "bool": {
                                "should": [
                                    {"term": {"appli_num.keyword": final_words["SQH"]}},  # 申请号
                                    {"term": {"appli_time.keyword": final_words["SQSJ"]}},  # 申请日
                                    {"term": {"patent_name.another": final_words["ZLMC"]}},  # 专利名称
                                    {"term": {"pub_num.keyword": final_words["GKH"]}},  # 公开号
                                    {"term": {"pub_time.keyword": final_words["GKSJ"]}},  # 公开日
                                    # {"term": {"cpc_classifi": final_words["CPC]}},       # CPC分类号
                                    {"term": {"ipc_classifi": final_words["IPC"]}},  # IPC分类号
                                    {"term": {"proposer": final_words["SQR"]}},  # 申请（专利权）人
                                    {"term": {"inventor": final_words["FMR"]}},  # 发明（设计）人
                                    # {"term": {"angent": final_words["DLR]}},                   # 代理人
                                    # {"term": {"angency": final_words["DLJG"]}},                 # 代理机构
                                    # {"term": {"patent_type": final_words["ZLLX"]}},         # 专利类型
                                    {"multi_match": {  # multi_match查询
                                        "query": key_words,  # 查询关键词
                                        "fields": ["patent_name.another",  # 专利名称
                                                   "proposer",  # 申请（专利权）人
                                                   "proposer_addr.another",  # 申请人地址
                                                   "inventor",  # 发明（设计）人
                                                   # "cpc_classifi",  # CPC分类号
                                                   "ipc_classifi",  # IPC分类号
                                                   "priority_num.keyword",  # 优先权号
                                                   "priority_time.keyword",  # 优先权日
                                                   "patent_abs.another",  # 摘要内容
                                                   ]  # 查询字段
                                    }},
                                    {"match": {"lang.keyword": language}},
                                    {"match": {"legel_status.another": legal_status}},
                                ],
                                "minimum_should_match": match
                            }
                        },
                        "aggs": {
                            "inv": {
                                "terms": {
                                    "field": "inventor",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "ipc": {
                                "terms": {
                                    "field": "ipc_classifi",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            },
                            "pro": {
                                "terms": {
                                    "field": "proposer",
                                    "size": 10,
                                    "order": {"_count": "desc"}
                                }
                            }
                        },
                        "highlight": {
                            "require_field_match": False,
                            "fields": {
                                  "patent_name.another": {},
                                  "appli_num.keyword": {},
                                  "appli_time.keyword": {},
                                  "proposer": {},
                                  "proposer_addr.another": {},
                                  "inventor": {},
                                  "patent_abs.another": {"number_of_fragments": 0}
                            },
                            "pre_tags": ['<span style="color:red;">'],  # 高亮开始标签
                            "post_tags": ['</span>'],  # 高亮结束标签
                        },
                        "from": (page - 1)*num,          # 从第几条开始获取
                        "size": num,                     # 获取多少条数据
                    }
                )
                return response
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response