from django.http import HttpResponse, StreamingHttpResponse, FileResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import io, os, mimetypes
import requests

def upload(request):
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, 'avatar-9.jpg')
    print(os.path.getsize(file_path))
    # with open(file_path, 'rb') as image:
    image = open(file_path, 'rb')
    
    content = image.read()
    # print(content)
    return HttpResponse(content, content_type = "image/jpg")

def default(request):
    r = requests.get("https://images.unsplash.com/photo-1452857576997-f0f12cd77844?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2850&q=80")
    with io.BytesIO() as buf:
        buf.write(r.content)
        
        return HttpResponse(r.content, content_type="image/jpg")
  
@csrf_exempt  
def home(request: HttpRequest):
    dir_name = os.path.dirname(__file__)
    if request.method == 'POST':
        file = request.FILES['img']
        file_path = os.path.join(dir_name, file.name)
        with open(file_path, 'wb') as image:
            image.write(file.read())
    return render(request, 'home.html')

def image_path(request, image_name):
    dir_name = os.path.dirname(__file__)
    file_path = os.path.join(dir_name, image_name)
    try:
        with open(file_path, 'rb') as image:
            ext = os.path.splitext(image.name)[-1][1:]
            print(ext)
            content = image.read()
        return HttpResponse(content, content_type=f'image/{ext}')
    except FileNotFoundError as e:
        return HttpResponse(f"{image_name} not found")