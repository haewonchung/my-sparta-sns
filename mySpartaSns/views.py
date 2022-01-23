from django.http import HttpResponse
from django.shortcuts import render
# render이라는 함수는 template에 있는 html 파일을 찾아서 보여줍니다!

def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!")

def first_view(request):
    return render(request, 'my_test.html')