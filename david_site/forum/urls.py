from django.urls import path, include
from . import views

'''
path converters:
example:

<int:variableName>

html:
{% url 'nameInPath' variableName=object.attribute %}

# BUG: Not able to use pathconveters in view functions properly
'''
urlpatterns = [
    path('', views.forum_home, name='forum-home'),
    path('<int:category_pk>/', views.forum_category, name='forum-category'),
    path('<int:category>/new/', views.forum_post, name='forum-new'),
    path('<int:category_id>/<int:post_pk>/detail/', views.forum_detail, name='forum-detail'),
    path('<int:category_id>/<int:post_id>/comment/', views.comment_vote, name='comment-vote'),
    path('<int:category_id>/<int:post_id>/post/', views.post_vote, name='post-vote'),
    path('<int:category_id>/<int:post_id>/delete/', views.delete_post, name='delete-post'),
    path('<int:category_id>/<int:post_pk>/post_edit/', views.forum_edit, name='forum-edit'),
    path('<int:category_id>/<int:post_id>/<int:comment_id>/comment_edit/', views.comment_edit, name='comment-edit'),
    path('<int:category_id>/<int:comment_id>/<int:post_id>/', views.delete_comment, name='delete-comment'),

    #new
    # path('<int:category_id>/<int:post_id>/<str:voteCount>/', views.vote, name='vote-post'),
    # path('<int:category_id>/<int:post_id>/<int:comment_id>/<str:voteCount>/', views.vote_comment, name='vote-comment'),
]
