from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    topic = models.CharField(max_length=100)
    description = models.CharField(blank=True, max_length=255)

    def __str__(self):
        return self.topic

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    post_vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_votes', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(blank=True, null=True)

    def total_post_vote(self):
        return self.post_vote.count()

    def __str__(self):
        return self.title

class Comment(models.Model):
    comment = models.TextField()
    comment_vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_votes', blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def total_comment_vote(self):
        return self.comment_vote.count()

    def __str__(self):
        return self.comment
