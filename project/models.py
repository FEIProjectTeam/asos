from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Post(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, related_name="posts"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)


def attachment_user_path(instance, filename):
    return "attachments/user_{0}/{1}".format(instance.post.author.id, filename)


class Attachment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to=attachment_user_path)


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", blank=True, null=True
    )
    text = models.TextField()


class LikeType(models.TextChoices):
    LIKE = "like", _("Like")
    HEART = "heart", _("Heart")
    LAUGH = "laugh", _("Laugh")


class Like(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes", blank=True, null=True
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes", blank=True, null=True
    )
    like_type = models.CharField(
        max_length=10, choices=LikeType.choices, default=LikeType.LIKE
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    Q(post__isnull=False, comment__isnull=True)
                    | Q(post__isnull=True, comment__isnull=False)
                ),
                name="exactly_one_of_post_or_comment",
            ),
        ]
