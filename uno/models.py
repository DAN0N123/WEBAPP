from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class UserPost(BaseModel):
    post_text = models.CharField(max_length=500)
    username = models.CharField(max_length = 100)
    likes = models.IntegerField(default=0, null=True, blank=True)
    dislikes = models.IntegerField(default=0, null=True, blank=True)
    who_liked = models.CharField(max_length=255, blank=True, null=True)
    who_disliked = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return str(self.pk)
    
    def add_like(self, user_id):
        liked_users = [int(id) for id in (self.who_liked or '').split(',') if id]
        disliked_users = [int(id) for id in (self.who_disliked or '').split(',') if id]

        if user_id in liked_users:
            self.likes -= 1
            liked_users.remove(user_id)
            self.who_liked = ','.join(map(str, liked_users))
        else:
            self.likes += 1
            liked_users.append(user_id)
            self.who_liked = ','.join(map(str, liked_users))

            if user_id in disliked_users:
                self.dislikes -= 1
                disliked_users.remove(user_id)
                self.who_disliked = ','.join(map(str, disliked_users))


    def add_dislike(self, user_id):
        liked_users = [int(id) for id in (self.who_liked or '').split(',')if id]
        disliked_users = [int(id) for id in (self.who_disliked or '').split(',')if id]

        if user_id in disliked_users:
            self.dislikes -= 1
            disliked_users.remove(user_id)
            self.who_disliked = ','.join(map(str, disliked_users))
        else:
            self.dislikes += 1
            disliked_users.append(user_id)
            self.who_disliked = ','.join(map(str, disliked_users))

            if user_id in liked_users:
                self.likes -= 1
                liked_users.remove(user_id)
                self.who_liked = ','.join(map(str, liked_users))


class Comment(BaseModel):
    user_post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments', default=None)
    commenter = models.CharField(max_length=100, default="")
    comment_text = models.CharField(max_length=500)
    def __str__(self):
        return str(self.pk)