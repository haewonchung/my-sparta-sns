from django.shortcuts import render, redirect
from .models import UserModel  # from . 이라는 것은 내가 가지고 있는 위치 = 나와 동등한 위치 ⇒ .models = 나와 동등한 위치의 models에서 가져옴
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import auth  # 사용자 auth 기능 | 장고의 auth 모델 (인증 찰;)
from django.contrib.auth.decorators import login_required


# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
        if user:  # 로그인이 되어있다면 sign up 보여주지 않고 ('/')인 tweet으로
            return redirect('/')
        else:  # 로그인이 되어있지 않다면 sign up으로
            return render(request, 'user/signup.html')
    elif request.method == 'POST':  # 데이터 베이스 저장 기능
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if password != password2:  # 비밀번호랑 비밀번호 확인이 안맞을 경우
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '':
                # 사용자 저장을 위한 username과 password가 필수라는 것을 얘기 해 줍니다.
                return render(request, 'user/signup.html', {'error': '사용자 이름과 패스워드는 필수 값 입니다'})

            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html',
                              {'error': '사용자가 존재합니다.'})  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')  # sign in page 의 name과 동일하게 작성해준다.
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)  # 장고 인증모델 사용해서 사용자 불러오기

        if me is not None:  # 사용자가 존재하는지
            auth.login(request, me)
            # return HttpResponse(f"{me.username}님 로그인 성공!")  # 그냥 username도 가능
            return redirect('/')  # tweet의 path('', views.home, name='home') -> def home(request):
        else:
            return render(request, 'user/signin.html', {'error': '유저 이름 혹은 패스워드를 확인 해 주세요'})  # 로그인 실패
    elif request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
        if user:  # 로그인이 되어있다면 sign up 보여주지 않고 ('/')인 tweet으로
            return redirect('/')
        else:  # 로그인이 되어있지 않다면 sign in으로
            return render(request, 'user/signin.html')


@login_required  # 로그인이 꼭 되어있어야 접근 가능한 함수다~! 위에서 login_required 임포트
def logout(request):
    auth.logout(request)  # 인증 되어있는 정보를 없애기
    return redirect("/")


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)  # exclude-리스트에서 내 이름은 빼줄거야~
        return render(request, 'user/user_list.html', {'user_list': user_list})  # 유저 리스트랑 같이 보여줄거야


@login_required
def user_follow(request, id):
    me = request.user  # 로그인 한 사람
    click_user = UserModel.objects.get(id=id)  # 로그인 한 사람이 클릭한 사람
    if me in click_user.followee.all():  # 그 사람이 팔로우 하는 모든 사람 중에 내가 있으면
        click_user.followee.remove(request.user)  # 나를 빼주고
    else:
        click_user.followee.add(request.user)  # 없다면 팔로우 할 것이다.
    return redirect('/user')
