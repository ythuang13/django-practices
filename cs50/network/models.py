from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def get_followers(self):
        """return query of followers"""
        return [x.follower for x in Follow.objects.all() if x.following == self]

    def get_following(self):
        """return query of following"""
        return [x.following for x in Follow.objects.all() 
                    if x.follower == self]

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post_user")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user}-{self.body[0:30]} {self.timestamp}"

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ['follower', 'following']

    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liked_user")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="liked_post")

    class Meta:
        unique_together = ['user', 'post']