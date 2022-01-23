from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect
from .models import TweetModel, TweetComment  # 글쓰기 모델 -> 가장 윗부분에 적어주세요!
from django.contrib.auth.decorators import login_required


# Create your views here.
# 유저가 로그인 했는지 확인 하고 안됐으면 로긴 페이지로 보내고 되면 트윗 화면으로
def home(request):
    user = request.user.is_authenticated  # 사용자가 인증을 받았는지 (로그인이 되어있는지)
    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')


# get 이면 트윗을 띄워줌
def tweet(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인이 되어 있는지 확인하기

        if user:  # 로그인 한 사용자라면 트윗으로
            all_tweet = TweetModel.objects.all().order_by('-created_at')  # 역순으로 출력
            return render(request, 'tweet/home.html', {'tweet': all_tweet})  # 딕셔너리로 넘겨주기
        else:  # 로그인이 되어 있지 않다면 로그인으로
            return redirect('/sign-in')
    elif request.method == 'POST':  # 요청 방식이 POST 일때
        user = request.user  # 현재 로그인 한 사용자를 불러오기
        content = request.POST.get('my-content', '')  # 글 작성이 되지 않았다면 빈칸으로
        tags = request.POST.get('tag', '').split(',')

        if content == '':  # 글이 빈칸이면 기존 tweet과 에러를 같이 출력
            all_tweet = TweetModel.objects.all().order_by('-created_at')
            return render(request, 'tweet/home.html',
                          {'error': '글은 공백일 수 없습니다', 'tweet': all_tweet})  # 긁어온 트윗도 같이 보여줘야 한다.
        else:
            my_tweet = TweetModel.objects.create(author=user, content=content)  # 글 저장을 한번에!
            for tag in tags:  # 태그들이 리스트로 와서
                tag = tag.strip()  # 공백 제거하고 넣기
                if tag != '':  # 태그를 작성하지 않았을 경우에 저장하지 않기 위해서
                    my_tweet.tags.add(tag)
            my_tweet.save()
            return redirect('/tweet')


@login_required  # 로그인 한 사람만 함수 실행할 수 있도록 하기
def delete_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)  # 특정 인자id만 불러오기
    my_tweet.delete()
    return redirect('/tweet')


@login_required
def detail_tweet(request, id):
    my_tweet = TweetModel.objects.get(id=id)
    tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
    return render(request, 'tweet/tweet_detail.html', {'tweet': my_tweet, 'comment': tweet_comment})


@login_required
def write_comment(request, id):
    if request.method == 'POST':
        comment = request.POST.get("comment", "")
        current_tweet = TweetModel.objects.get(id=id)

        TC = TweetComment()
        TC.comment = comment
        TC.author = request.user
        TC.tweet = current_tweet
        TC.save()

        return redirect('/tweet/' + str(id))


@login_required
def delete_comment(request, id):
    comment = TweetComment.objects.get(id=id)
    current_tweet = comment.tweet.id
    comment.delete()
    return redirect('/tweet/' + str(current_tweet))


# 태그가 있으면 보여주겠다 - 공식 문서대로 작성됨
class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
