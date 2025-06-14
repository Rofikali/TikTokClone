from django.conf import settings
from comments.serializers import CommentSerializer
from like.serializers import LikeSerializer
from rest_framework import serializers
from .models import Post
from django.contrib.auth import get_user_model

user = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    video = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "text", "video", "created_at", "comments", "likes", "user"]
        depth = 2
        # fields = ["id", "text", "video", "created_at","likes", "user"]

    # def get_user(self, obj):
    #     request = self.context.get("request")
    #     return {
    #         "id": obj.user.id,
    #         "name": obj.user.name,
    #         "email": obj.user.email,
    #         "image": request.build_absolute_uri(obj.user.image.url) if request else f"{settings.MEDIA_URL}{obj.user.image.url}'",
    #         # 'image': request.build_absolute_uri(obj.user.image.url) if request else f"{settings.MEDIA_URL}{obj.user.image.url}"
    #     }

    def get_user(self, obj):
        request = self.context.get("request")
        user = obj.user

        image_url = None
        if hasattr(user, "image") and user.image:
            if request:
                image_url = request.build_absolute_uri(user.image.url)
            else:
                image_url = f"{settings.MEDIA_URL}{user.image.url}"

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "image": image_url,
        }

    def get_video(self, obj):
        request = self.context.get("request")

        video_url = None
        if hasattr(obj, "video") and obj.video:  # Safely check the video exists
            try:
                if request:
                    video_url = request.build_absolute_uri(obj.video.url)
                else:
                    video_url = f"{settings.MEDIA_URL}{obj.video.url}"
            except ValueError:
                # This catches cases like "The 'video' attribute has no file associated with it."
                video_url = None

        return video_url

    # def get_video(self, obj):

    #     if obj.video:
    #         print("obj is comming ---->>>", obj)
    #         request = self.context.get("request")
    #         return (
    #             request.build_absolute_uri(obj.video.url)
    #             if request
    #             else f"{settings.MEDIA_URL}{obj.video.url}"
    #         )
    #     return None

    def get_created_at(self, obj):
        return obj.created_at.strftime("%b %d %Y")
