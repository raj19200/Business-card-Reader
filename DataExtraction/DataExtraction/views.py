from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import sys
from subprocess import run,PIPE

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
    image= run([sys.executable,'F://Visual Studio Code//djangoproject//main.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)
    # print("final text",image.stdout)
    params={"text":image.stdout}
    return render(request,'home.html',params)

def test(request):
    fname="raj"
    number="9103654789"
    params={"fname":fname,"number":number}
    return render(request,'test.html',params)

def test2(request):
    return HttpResponse("done")