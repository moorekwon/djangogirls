from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.models import Post


def post_list(request):
    # 상위 폴더(blog)의
    # 상위 폴더(djangogirls)의
    # 하위폴더(templates)의
    # 하위파일(post_list.html)
    # 내용을 read()한 결과를 HttpResponse에 인자로 전달

    # 경로 이동
    # os.path.abspath(__file__) <- 현재 파일의 절대 경로를 리턴해줌
    # os.path.dirname
    # os.path.join

    # 파일 열기
    # open
    # cur_file_path = os.path.abspath(__file__)
    # blog_dir_path = os.path.dirname(cur_file_path)
    # root_dir_path = os.path.dirname(blog_dir_path)
    # templates_dir_path = os.path.join(root_dir_path, 'templates')
    # post_list_html_path = os.path.join(templates_dir_path, 'post_list.html')
    #
    # # print(cur_file_path)
    # # print(blog_dir_path)
    #
    # print(templates_dir_path)
    # # /home/hyojinkwon/projects/wps12th/djangogirls/templates
    #
    # f = open(post_list_html_path, 'rt')
    # html = f.read()
    # f.close()
    #
    # return HttpResponse(html)

    # posts라는 변수에 전체 Post를 갖는 QuerySet 객체를 전달
    # Post.objects.무언가...를 실행한 결과는 QuerySet 객체가 됨
    # context라는 dict를 생성하며 'posts' 키에 위 posts 변수를 value로 사용하도록 함
    # render의 3번째 위치인자로 위 context 변수를 전달

    # posts = Post.objects.all()
    # 역순
    posts = Post.objects.order_by('-pk')
    context = {
        'posts': posts
    }

    # Template을 찾을 경로에서 post_list.html을 찾아 text로 만들고 HttpResponse 형태로 돌려줌
    # shortcut 함수
    return render(request, 'post_list.html', context)


def post_detail(request, pk):
    # 이 view 함수의 매개변수로 전달되는 'pk'를 사용
    # 전달받은 'pk' 값이 자신의 'pk' DB column 값과 같은 Post를 post 변수에 저장
    # 이후 pk에 따라 /post-detail/에 접근했을 때, 다른 Post가 출력되는지 확인
    # posts = Post.objects.filter(pk=pk)
    # post = posts[0]

    # try-except 구문 사용
    # pk에 해당하는 Post가 없는 경우, HttpResponse('없음')을 돌려주도록 함
    try:
        post = Post.objects.get(pk=pk)
    except:
        return HttpResponse('없음!')

    post = get_object_or_404(Post, pk=pk)

    # URL: /post-detail/
    # View: post_detail
    # Template: post_detail.html

    # 전체 Post 목록(Post 전체 QuerySet) 중 [0] index에 해당하는 Post 객체 하나를 post 변수에 할당
    # post = Post.objects.all()[0]
    # 'context'라는 이름의 dict를 만들어 'post' key 위에 위 post 변수를 value로 사용
    context = {
        'post': post
    }
    # 이 context 변수를 render의 3번째 인자로 전달
    # post_detail.html에서는 전달받은 'post' 변수의 title, author, text, created_date, published_date를 출력

    return render(request, 'post_detail.html', context)


def post_add(request):
    # print(request.POST)

    # 요청의 method에 따라서 분기
    if request.method == 'POST':
        # request.POST에 담긴 title, text를 HttpResponse를 사용해 리턴
        # title: <입력받은 제목>, text: <입력받은 텍스트>
        # 위 문자열 리턴
        author = request.user
        title = request.POST['title']
        text = request.POST['text']
        # print(title, text)

        # 위 3개 값을 사용해 새로운 Post 생성
        # 생성한 Post의 title, created_date를 HttpResponse에 문자열로 전달
        post = Post.objects.create(
            author=author,
            title=title,
            text=text
        )

        result = f'title: {post.title}, created_date: {post.created_date}'
        # return HttpResponse(result)
        from django.urls import reverse
        # post_list_url = reverse('url-name-post-list')
        # return HttpResponseRedirect('post_list_url')
        return redirect('url-name-post-list')
    else:
        # URL: /posts/add/
        # View: post_add 함수
        # Template: post_add.html
        # form 태그 내부에
        # input 한 개, textarea 한 개, button[type=submit] 한 개

        # base.html의 nav 안에 /posts/add/로의 링크 하나 추가
        # 링크 텍스트: Post Add
        return render(request, 'post_add.html')


def post_delete_confirm(request, pk):
    #     "정말 이 글을 삭제하시겠습니까?"
    #     글 제목과 작성일자 보여줌
    #     delete 버튼 한번더 누르면 삭제 후 post-list로 redirect
    post = Post.objects.get(pk=pk)
    context = {
        'post': post
    }
    return render(request, 'post_delete_confirm.html', context)


def post_delete(request, pk):
    # # pk에 해당하는 Post 삭제
    # # 삭제 후 post_list 페이지로 이동
    # post = Post.objects.filter(pk=pk)
    # # print(post)
    # post.delete()
    #
    # # return render(request, 'post_list.html')
    # return redirect('url-name-post-list')

    #     답안
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('url-name-post-list')


def post_edit(request, pk):
    # pk에 해당하는 Post 수
    # if request.method == 'POST':
    #     # request.POST로 전달된 title, text 내용 사용
    #     # pk에 해당하는 Post의 해당 필드를 수정하고 save()
    #     # 이후 해당 Post의 post-detail 화면으로 이동
    #     post = Post.objects.get(pk=pk)
    #
    #     title = request.POST['title']
    #     text = request.POST['text']
    #     # print(f'title: {title}, text: {text}')
    #
    #     post.title = title
    #     post.text = text
    #     post.save()
    #
    #     return redirect('url-name-post-detail', pk)
    #
    # else:
    #     # 수정할 수 있는 form이 존재하는 화면을 보여줌
    #     # 화면의 form에는 pk에 해당하는 Post의 title, text 값이 들어있어야 함(수정이므로)
    #     post = Post.objects.get(pk=pk)
    #     context = {
    #         'post': post
    #     }
    #     print(post)
    #     return render(request, 'post_edit.html', context)

    # 답안
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']

        post = Post.objects.get(pk=pk)

        post.title = title
        post.text = text
        post.save()

        return redirect('url-name-post-detail', pk=pk)
    else:
        post = Post.objects.get(pk=pk)
        context = {
            'post': post
        }
        return render(request, 'post_edit.html', context)


def post_publish(request, pk):
    # pk에 해당하는 Post의 published_date 업데이트
    # 요청시점의 시간을 해당 Post의 published_date에 기록할 수 있도록 함
    # 완료 후 post-detail로 이동
    # 결과를 볼 수 있도록 리스트 및 디테일 홤녀에서 published_date도 출력하도록 함
    post = Post.objects.get(pk=pk)
    post.published_date = timezone.now()
    post.save()
    return redirect('url-name-post-detail', pk=pk)


def post_unpublish(request, pk):
    # pk에 해당하는 Post의 published_date에 None 대입 후 save()
    # 완료 후 post-detail로 이동
    # 결과를 볼 수 있도록, 리스트 및 디테일 화면에서 published_date 출력하도록 함
    post = Post.objects.get(pk=pk)
    post.published_date = None
    post.save()
    return redirect('url-name-post-detail', pk=pk)
    pass
