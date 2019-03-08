#coding=UTF-8
# Create your views here.
from .models import LawRegulate
import json
from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.db.models import Q

def index(request):
    return render(request, 'sitesearch/index.html')

def law_index(request):
    try:
        print("lawstart")
        # 反垄断法
        antitrust_list = {}
        antilaw_search = LawRegulate.objects.filter(Q(json_tile='antitrust_law.json') & Q(category='法律'))
        antilaw_information = json.loads(serializers.serialize("json", antilaw_search))
        a = []
        for n in antilaw_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        antitrust_list["law"] = a

        a = []
        antistate_search = LawRegulate.objects.filter(Q(json_tile='antitrust_law.json') & Q(category='国务院部门规章'))
        antistate_information = json.loads(serializers.serialize("json", antistate_search))
        for n in antistate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        antitrust_list["state"] = a

        # 著作权
        copyright_list = {}
        copylaw_search = LawRegulate.objects.filter(Q(json_tile='copyright_law.json') & Q(category='法律'))
        copylaw_information = json.loads(serializers.serialize("json", copylaw_search))
        a = []
        for n in copylaw_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        copyright_list["law"] = a

        a = []
        copyadmin_search = LawRegulate.objects.filter(Q(json_tile='copyright_law.json') & Q(category='行政法规'))
        copyadmin_information = json.loads(serializers.serialize("json", copyadmin_search))
        for n in copyadmin_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        copyright_list["admin"] = a

        a = []
        copystate_search = LawRegulate.objects.filter(Q(json_tile='copyright_law.json') & Q(category='国务院部门规章'))
        copystate_information = json.loads(serializers.serialize("json", copystate_search))
        for n in copystate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        copyright_list["state"] = a

        a = []
        copyregul_search = LawRegulate.objects.filter(Q(json_tile='copyright_law.json') & Q(category='地方性法规'))
        copyregul_information = json.loads(serializers.serialize("json", copyregul_search))
        for n in copyregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        copyright_list["regulations"] = a

        a = []
        copyregul_search = LawRegulate.objects.filter(Q(json_tile='copyright_law.json') & Q(category='地方政府规章'))
        copyregul_information = json.loads(serializers.serialize("json", copyregul_search))
        for n in copyregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        copyright_list["govregulations"] = a


        # 域名法
        domain_list = {}
        domainstate_search = LawRegulate.objects.filter(Q(json_tile='domain_name_law.json') & Q(category='国务院部门规章'))
        domainstate_information = json.loads(serializers.serialize("json", domainstate_search))
        a = []
        for n in domainstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        domain_list["state"] = a


        # 地理标志法
        geographical_list = {}
        geographicalstate_search = LawRegulate.objects.filter(Q(json_tile='geographical_indication_law.json') & Q(category='国务院部门规章'))
        geographicalstate_information = json.loads(serializers.serialize("json", geographicalstate_search))
        a = []
        for n in geographicalstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        geographical_list["state"] = a


        # 集成电路法
        integrated_list = {}
        integratedstate_search = LawRegulate.objects.filter(Q(json_tile='integrated_circuit_law.json') & Q(category='国务院部门规章'))
        integratedstate_information = json.loads(serializers.serialize("json", integratedstate_search))
        a = []
        for n in integratedstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        integrated_list["state"] = a

        # 植物新品种
        new_plant_list = {}

        a = []
        new_plantadmin_search = LawRegulate.objects.filter(Q(json_tile='new_plant_species_law.json') & Q(category='行政法规'))
        new_plantadmin_information = json.loads(serializers.serialize("json", new_plantadmin_search))
        for n in new_plantadmin_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        new_plant_list["admin"] = a

        a = []
        new_plantstate_search = LawRegulate.objects.filter(Q(json_tile='new_plant_species_law.json') & Q(category='国务院部门规章'))
        new_plantstate_information = json.loads(serializers.serialize("json", new_plantstate_search))
        for n in new_plantstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        new_plant_list["state"] = a

        a = []
        new_plantregul_search = LawRegulate.objects.filter(Q(json_tile='new_plant_species_law.json') & Q(category='地方性法规'))
        new_plantregul_information = json.loads(serializers.serialize("json", new_plantregul_search))
        for n in new_plantregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        new_plant_list["regulations"] = a

        # 专利法
        patent_list = {}
        patentlaw_search = LawRegulate.objects.filter(Q(json_tile='patent_law.json') & Q(category='法律'))
        patentlaw_information = json.loads(serializers.serialize("json", patentlaw_search))
        a = []
        for n in patentlaw_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        patent_list["law"] = a

        a = []
        patentadmin_search = LawRegulate.objects.filter(Q(json_tile='patent_law.json') & Q(category='行政法规'))
        patentadmin_information = json.loads(serializers.serialize("json", patentadmin_search))
        for n in patentadmin_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        patent_list["admin"] = a

        a = []
        patentstate_search = LawRegulate.objects.filter(Q(json_tile='patent_law.json') & Q(category='国务院部门规章'))
        patentstate_information = json.loads(serializers.serialize("json", patentstate_search))
        for n in patentstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        patent_list["state"] = a

        a = []
        patentregul_search = LawRegulate.objects.filter(Q(json_tile='patent_law.json') & Q(category='地方性法规'))
        patentregul_information = json.loads(serializers.serialize("json", patentregul_search))
        for n in patentregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        patent_list["regulations"] = a

        a = []
        patentregul_search = LawRegulate.objects.filter(Q(json_tile='patent_law.json') & Q(category='地方政府规章'))
        patentregul_information = json.loads(serializers.serialize("json", patentregul_search))
        for n in patentregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        patent_list["govregulations"] = a

        # 软件著作权
        software_list = {}
        a = []
        softwarestate_search = LawRegulate.objects.filter(Q(json_tile='software_copyright_law.json') & Q(category='国务院部门规章'))
        softwarestate_information = json.loads(serializers.serialize("json", softwarestate_search))
        for n in softwarestate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        software_list["state"] = a

        a = []
        softwareregul_search = LawRegulate.objects.filter(Q(json_tile='software_copyright_law.json') & Q(category='地方性法规'))
        softwareregul_information = json.loads(serializers.serialize("json", softwareregul_search))
        for n in softwareregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        software_list["regulations"] = a

        # 商标法
        trademark_list = {}
        trademark_search = LawRegulate.objects.filter(Q(json_tile='trademark_law.json') & Q(category='法律'))
        trademark_information = json.loads(serializers.serialize("json", trademark_search))
        a = []
        for n in trademark_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        trademark_list["law"] = a

        a = []
        trademarkadmin_search = LawRegulate.objects.filter(Q(json_tile='trademark_law.json') & Q(category='行政法规'))
        trademarkadmin_information = json.loads(serializers.serialize("json", trademarkadmin_search))
        for n in trademarkadmin_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        trademark_list["admin"] = a

        a = []
        trademarkstate_search = LawRegulate.objects.filter(Q(json_tile='trademark_law.json') & Q(category='国务院部门规章'))
        trademarkstate_information = json.loads(serializers.serialize("json", trademarkstate_search))
        for n in trademarkstate_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        trademark_list["state"] = a

        a = []
        trademarktregul_search = LawRegulate.objects.filter(Q(json_tile='trademark_law.json') & Q(category='地方性法规'))
        trademarkregul_information = json.loads(serializers.serialize("json", trademarktregul_search))
        for n in trademarkregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        trademark_list["regulations"] = a

        a = []
        trademarkregul_search = LawRegulate.objects.filter(Q(json_tile='trademark_law.json') & Q(category='地方政府规章'))
        trademarkregul_information = json.loads(serializers.serialize("json", trademarkregul_search))
        for n in trademarkregul_information:
            b = {}
            b["id"] = n["fields"]["law_id"]
            b["category"] = n["fields"]["category"]
            b["law_title"] = n["fields"]["law_title"]
            b["json_tile"] = n["fields"]["json_tile"]
            b["publish_time"] = n["fields"]["publish_time"]
            b["effect_time"] = n["fields"]["effect_time"]
            a.append(b)
        trademark_list["govregulations"] = a
        print("lawend")
        return render(request, 'law_regulate/laws.html', {'antitrust_list': antitrust_list,
                                                          'copyright_list':copyright_list,
                                                          'domain_list':domain_list,
                                                          'geographical_list':geographical_list,
                                                          'integrated_list':integrated_list,
                                                          'new_plant_list':new_plant_list,
                                                          'patent_list':patent_list,
                                                          'software_list':software_list,
                                                          'trademark_list':trademark_list})
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

def law_detail(request):
    try:
        print("lawdetailstart")
        laws_id = request.GET.get('laws_id')
        json_title = request.GET.get('json_title')
        if (not laws_id) and (not json_title):
            return render(request,'sitesearch/index.html')
        else:
            search_list = LawRegulate.objects.filter(Q(law_id=laws_id) & Q(json_tile=json_title))
            detail_information = json.loads(serializers.serialize("json", search_list))
            print(detail_information)
            print("lawdetailend")
            return render(request, 'law_regulate/laws_details.html', {'law_information': detail_information})
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

def law_search(request):
    try:
        print("lawsearchstart")
        law_title = request.GET.get('law_title')
        if not law_title:
            return render(request,'sitesearch/index.html')
        else:
            search_result = LawRegulate.objects.filter(law_title=law_title)
            law_information = json.loads(serializers.serialize("json", search_result))
            print("lawsearchend")
            return render(request, 'law_regulate/laws_search.html', {'law_information': law_information,
                                                                     'law_title': law_title})
    except Exception as e:
        print(e)
        response = HttpResponse(json.dumps({"msg": e}), content_type='application/json')
        response['Access-Control-Allow-Origin'] = '*'
        return response

