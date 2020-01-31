from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.utils import timezone

# Create your views here.
def forum_edit(request, category_id, post_pk):
    '''
    get_object_or_404(Model, attribute={some parameter which will link to an individual object})
    '''
    post = get_object_or_404(Post, id=post_pk) #set post variable to specific post object

    #if user attempts to submit form (POST METHOD)
    if request.method == "POST": #<== this is only triggered when the user attempts to update form (updates content via forms and presses update button)

        #place updated content from form with current object in variable

        form_edit = PostForm(request.POST, instance=post)

        #if the updated object data is_valid continue
        if form_edit.is_valid():
            post = form_edit.save(commit=False)
            post.modified_date = timezone.now()
            #save the updated content into specific object
            post.save()

            #redirect the user to post-object page
            return redirect('forum-detail', category_id=category_id, post_pk=post_pk)

    #First time loading page will load specified object inside form
    else: #<--- only triggered when the edit post button is pressed, this will trigger a GET request, which will load the object data in a form.
        form_edit = PostForm(instance=post)

    context = {
        "form_edit": form_edit,
    }
    return render(request, 'forum/edit_post.html', context)

    #NEW Edit comments

def comment_edit(request, category_id, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        comment_edit = CommentForm(request.POST, instance=comment)
        if comment_edit.is_valid():
            comment = comment_edit.save(commit=False)
            comment.modified_date = timezone.now()
            comment.save()
            return redirect('forum-detail', category_id=category_id, post_pk=post_id)
    else:
        comment_edit = CommentForm(instance=comment)

    context = {
        'comment_edit': comment_edit,
    }
    return render(request, 'forum/edit_comment.html', context)


def forum_home(request):
    context = {
        'categories': Category.objects.all(),
    }

    return render(request, 'forum/forum_home.html', context)

def forum_category(request, category_pk):
    context = {
        'posts': Post.objects.filter(category=category_pk).order_by('-posted_date'),
        'category': Category.objects.get(pk=category_pk),
    }
    return render(request, 'forum/forum_listing.html', context)

def forum_detail(request, category_id , post_pk):
    #Initiate comment_like + total_comment list
    comment_like, total_comment = [], []

    #Retrieve specific post object
    post = get_object_or_404(Post, id=post_pk)

    #Retrieve specific comments associated to Post object
    if Comment.objects.filter(post=post_pk):
        comments = get_list_or_404(Comment, post=post_pk)

        #iterate through comment objects associated to post
        for comment in comments:
            if comment.comment_vote.filter(id=request.user.id).exists():
                comment_like.append(True)
            else:
                comment_like.append(False)
            total_comment.append(comment.total_comment_vote())
        #Reverse list order to match descending comments (newest - bottom)
        comment_like.reverse()
        total_comment.reverse()
    else:
        comments = None

    #Initialize boolean on page load
    post_like = False

    #If user voted on post set post_like=True
    if post.post_vote.filter(id=request.user.id).exists():
        post_like = True





    '''
    NEW def forum_detail(request, category_id, post_pk):
        form = CommentForm(request.POST or None)
        Equates to...
        if form = CommentForm(request.POST):
            if request.method == "POST":
                Data inside form and was submitted
        else:
            form = CommentForm() <-- Display empty Comment form
    '''

    form = CommentForm(request.POST or None)
    if form.is_valid():
        '''
            form.save(commit=False)
            stores data that was collected from form, but requires that additional data be collected
            before being able to commit the row to the database,

            for instance,

        Model    |Comment  |vote          |posted_date    |author |post
        FieldType|TextField|IntegerField  |DateTimeField  |FK     |FK
        Form     |Yes      |No            |No             |No     |No
        Required?|Yes      |No            |No             |Yes    |Yes
        '''
        comment=form.save(commit=False)
        comment.author = request.user
        comment.post = Post.objects.get(pk=post_pk)
        comment.save()
        return redirect('forum-detail', category_id=category_id , post_pk=post_pk)

    context = {
        'category': Category.objects.get(pk=category_id),
        'post_detail': Post.objects.get(pk=post_pk),
        'post_comments': Comment.objects.filter(post=post_pk).order_by('-posted_date'),
        # 'post_comments': post_comments,
        'form' : form,
        'post_like': post_like,
        'comment_like': comment_like,
        'total_post_vote': post.total_post_vote(),
        'total_comment': total_comment,
        # 'total_comment_vote' : comments.total_comment_vote(),
    }

    return render(request, 'forum/forum_detail.html', context)

def forum_post(request, category):
    #Bound data to form, must be validated
    form = PostForm(request.POST or None)

    #If bound data is valid to model fields
    if form.is_valid():

        post = form.save(commit=False)
        post.author = request.user
        post.category = Category.objects.get(pk=category)
        post.save()
        return redirect('forum-detail', category_id=category, post_pk=post.pk)

    return render(request, 'forum/forum_edit.html', {'form': form})


def delete_comment(request, category_id , comment_id , post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author == request.user:
        if request.method == "POST":
            comment.delete()
            return redirect('forum-detail', category_id=category_id ,post_pk=post_id)
    context = {
        "comment": comment,
    }
    return render(request, 'forum/forum_detail.html')

# def delete_post(request, category_id, post_id):
def delete_post(request, category_id, post_id):
    post = get_object_or_404(Post, id=post_id)
    category_match = get_object_or_404(Category, id=category_id)
    if post.author == request.user:
        if request.method == "POST":
            post.delete()
            # return redirect('forum-category', category=category, category_pk=category_id)
            # return redirect('forum-category', category=category_match.topic, category_pk=category_id)
            return redirect('forum-category', category_pk=category_id)
    context = {
        'posts': Post.objects.filter(category=category_id).order_by('-posted_date'),
        'category': Category.objects.get(pk=category_match),
    }
    return render(request, 'forum/forum_listing.html', context)

'''
Old comment system, impossible to distinguish which users have already voted:

def vote(request, category_id, post_id, voteCount):
    # post = get_object_or_404(Post, post_id)
    vote = Post.objects.get(id=post_id)
    if request.method == 'POST':
        if voteCount == 'voteup':
            vote.vote += 1
            vote.save()
            return redirect('forum-detail', category_id=category_id, post_pk=post_id)
        elif voteCount == 'votedown':
            vote.vote += -1
            vote.save()
            return redirect('forum-detail', category_id=category_id, post_pk=post_id)
    context = {
        'category_id': Category.objects.get(pk=category_id),
        'post_pk': Post.objects.get(pk=post_id),
    }
    return render(request, 'forum/forum_detail.html', context)

def vote_comment(request, category_id, post_id, comment_id, voteCount):
    vote = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        if voteCount == 'voteup':
            vote.vote += 1
            vote.save()
            return redirect('forum-detail', category_id=category_id, post_pk=post_id)
        elif voteCount == 'votedown':
            vote.vote -= 1
            vote.save()
            return redirect('forum-detail', category_id=category_id, post_pk=post_id)
    context = {
        'category_id': Category.objects.get(pk=category_id),
        'post_pk': Post.objects.get(pk=post_id),
    }
    return render(request, 'forum/forum_detail.html', context)
'''

#New comment system CAN distinguish which users have already voted
def post_vote(request, category_id, post_id):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    post_like = False
    if post.post_vote.filter(id=request.user.id).exists():
        post_like = False
        post.post_vote.remove(request.user)
    else:
        post_like = True
        post.post_vote.add(request.user)
    return redirect('forum-detail', category_id=category_id, post_pk=post_id)

def comment_vote(request, category_id, post_id):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    comment_like = False
    if comment.comment_vote.filter(id=request.user.id).exists():
        comment_like = False
        comment.comment_vote.remove(request.user)
    else:
        comment_like = True
        comment.comment_vote.add(request.user)
    return redirect('forum-detail', category_id=category_id, post_pk=post_id)
