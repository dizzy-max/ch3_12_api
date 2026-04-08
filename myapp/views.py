from django.shortcuts import render
from django.http import HttpResponse
from myapp.models import *
from django.forms.models import model_to_dict
# Create your views here.

def search_list(request):
    if'cname' in request.GET:
        cname = request.GET['cname']
        print(cname)
        resultList = students.objects.filter(cname__contains=cname)
    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))
    # return HttpResponse("hello,this is search list page")
    errormessage=""
    # resultList=[]

    if not resultList:
        errormessage="No data found"
    # return render(request, 'search_list.html', locals())
    return render(request, 'search_list.html', {'resultList':resultList, 'errormessage':errormessage})

def search_name(request):
    return render(request, 'search_name.html')

from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search=site_search.strip()
        keywords=site_search.split()
        print(keywords)
        # resultList = students.objects.filter(cname__contains=site_search).order_by('cid')
        # resultList = students.objects.filter(
        #     Q(cid__contains=site_search) |
        #     Q(cname__contains=site_search) |
        #     Q(cbirthday__contains=site_search) |
        #     Q(cemail__contains=site_search) |
        #     Q(cphone__contains=site_search) |
        #     Q(caddr__contains=site_search)
        # )
        query = Q()
        for keyword in keywords:
            query |= Q(cid__contains=keyword) |Q(cname__contains=keyword) |Q(cbirthday__contains=keyword) |Q(cemail__contains=keyword) | Q(cphone__contains=keyword) | Q(caddr__contains=keyword)
        resultList = students.objects.filter(query).order_by('cid')
    else:
        resultList = students.objects.all().order_by('cid')

    for item in resultList:
        print(model_to_dict(item))
    data_count = len(resultList)
    print(f"Total data count: {data_count}")
    status=True
    errormessage=""
    if not resultList:
        status=False
        errormessage="No data found"
    # 分頁設定，每頁顯示2筆資料
    paginator = Paginator(resultList, 2)
    page_nmber = request.GET.get('page')  # 獲取當前頁碼
    page_obj = paginator.get_page(page_nmber)  # 獲取當前頁的資料
    print(f"page_nmber={page_nmber}")
    for item in page_obj:
        print(model_to_dict(item))

    return render(request, 'index.html',
                {
                'resultList': resultList,
                'status': status,
                'errormessage': errormessage,
                'data_count': data_count,
                'page_obj':page_obj
                }
    )
    

from django.shortcuts import redirect
def post(request):
    if request.method=="POST":
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        add=students(cname=cname, csex=csex, cbirthday=cbirthday, cemail=cemail, cphone=cphone, caddr=caddr)
        add.save()
        # return HttpResponse("已送出post")
        return redirect('index')
    else:
        return render(request, 'post.html')
    
def edit(request, id):
    print(id)
    if request.method=="POST":
        cname = request.POST.get('cname')
        csex = request.POST.get('csex')
        cbirthday = request.POST.get('cbirthday')
        cemail = request.POST.get('cemail')
        cphone = request.POST.get('cphone')
        caddr = request.POST.get('caddr')
        print(f"Received POST data: cname={cname}, csex={csex}, cbirthday={cbirthday}, cemail={cemail}, cphone={cphone}, caddr={caddr}")
        update = students.objects.get(cid=id)
        update.cname = cname
        update.csex = csex
        update.cbirthday = cbirthday
        update.cemail = cemail
        update.cphone = cphone
        update.caddr = caddr
        update.save()
        # return HttpResponse("已送出post")
        return redirect('index')
    else:
        obj = students.objects.get(cid=id)
        print(model_to_dict(obj))
        # return HttpResponse("edit")
        return render(request, 'edit.html',{'obj':obj})
    
def delete(request, id):
    if request.method=="POST":
        obj = students.objects.get(cid=id)
        obj.delete()
        print(model_to_dict(obj))
        return redirect('index')
        # return HttpResponse("已送出post")
    else:
        obj = students.objects.get(cid=id)
        # print(model_to_dict(obj))
        return render(request, 'delete.html',{'obj':obj})

from django.http import JsonResponse
def getAllitems(request):
    resultObject = students.objects.all().order_by('cid')
    # print(type(resultObject))
    resultList = list(resultObject.values())
    # print(type(resultList))
    # for i in resultList:
    #     print(type(i))
    # return HttpResponse("getAllitems")
    return JsonResponse(resultList, safe=False)

def getItem(request,id):
    try:
        obj = students.objects.get(cid=id)
        # print(type(obj))
        resultDict = model_to_dict(obj)
        return JsonResponse(resultDict, safe=False)
    except:
        return JsonResponse({"error":"item not found"}, status=404)