from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
from subprocess import run,PIPE
from .models import Result
from .main_ import test
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def index(request):
    return render(request,'home.html')
def demo(request):
    image=request.FILES['image']
    fs=FileSystemStorage()
    filename=fs.save(image.name,image)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    print("raw url",filename)
    print("file url",fileurl)
    print("template url",templateurl)
    contacts,pincode,email,website,city,state,address,name,path,companyname=test(filename)
    
    # image= run([sys.executable,'F://Visual Studio Code//djangoproject//main_.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)
    # print("final text",image.stdout)
    sep=" "
    def converttostr(input_seq, seperator):
        final_str = seperator.join(input_seq)
        return final_str
    def remove(string):
        return string.replace(" ","")
    name=converttostr(name,sep)
    name=remove(name)
    companyname=converttostr(companyname,sep)
    company_name=companyname
    email=converttostr(email,sep)
    website=converttostr(website,sep)
    contact1,contact2="",""
    if(len(contacts)):
        contact1=contacts[0]
        if(len(contacts)>1):
            contact2=contacts[1]
    else:
        contact1,contact2=" "," "
    contact1=remove(contact1)
    contact2=remove(contact2)
    city=converttostr(city,sep)
    state=converttostr(state,sep)
    pincode=converttostr(pincode,sep)
    address=converttostr(address,sep)
    address=remove(address)
    print(name,email,website,contact1,contact2,city,state,pincode,address)
    print("path",path)
    params={"name":name,"companyName":company_name,"email":email,"website":website,"contact1":contact1,"contact2":contact2,"city":city,"state":state,"pincode":pincode,"address":address,"fileurl":path,"filename":filename}
    print(params)
    return render(request,'show.html',params)
def show(request):
    if request.method=="POST":
        name=request.POST.get('name', " ")
        company_name=request.POST.get('cname', " ")
        email=request.POST.get('email', " ")
        website=request.POST.get('website', " ")
        contact1=request.POST.get('contact1', " ")
        contact2=request.POST.get('contact2', " ")
        city=request.POST.get('city', " ")
        state=request.POST.get('state', " ")
        pincode=request.POST.get('pincode', " ")
        address=request.POST.get('address', " ")
        fileurl=request.POST.get('fileurl', " ")
        filename=request.POST.get('filename', " ")
        card1=Result(name=name,company_name=company_name,email=email,website=website,contact1=contact1,contact2=contact2,city=city,state=state,pincode=pincode,address=address,fileurl=fileurl,filename=filename)
        card1.save()
    return render(request,"home.html")

def detail(request):
    allcard=Result.objects.all()
    allpost=Paginator(Result.objects.all(),4)   #show 5 result per page
    page=request.GET.get('page')
    try:
        posts=allpost.page(page)
    except PageNotAnInteger:
        posts=allpost.page(1)
    except EmptyPage:
        posts=allpost.page(allpost.num_pages)
    params={"allcard":allcard,"posts":posts}
    return render(request,"card.html",params)
def edittemp(request,id):
    abc=Result.objects.get(pk=id)
    params={"id":abc.id,"name":abc.name,"company":abc.company_name,'email':abc.email,'website':abc.website,'contact1':abc.contact1,"address":abc.address,"fileurl":abc.fileurl,"filename":abc.filename}
    return render(request,"edit.html",params)
def update(request,id):
    if request.method=="POST":
        name=request.POST.get('name', " ")
        company_name=request.POST.get('cname', " ")
        email=request.POST.get('email', " ")
        website=request.POST.get('website', " ")
        contact1=request.POST.get('contact1', " ")
        address=request.POST.get('address', " ")
        Result.objects.filter(pk=id).update(name=name,company_name=company_name,email=email,website=website,contact1=contact1,address=address) 
    return HttpResponseRedirect("/detail")
def search(request):
    query=request.GET['search']
    posttitle=Result.objects.filter(name__icontains=query)
    postcontent=Result.objects.filter(company_name__icontains=query)
    postcontent1=Result.objects.filter(address__icontains=query)
    postcontent2=Result.objects.filter(contact1__icontains=query)
    postcontent3=Result.objects.filter(email__icontains=query)
    post1=posttitle.union(postcontent)
    post2=post1.union(postcontent1)
    post3=post2.union(postcontent2)
    post=post3.union(postcontent3)
    params={'post':post}
    return render(request,"search.html",params)