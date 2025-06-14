from ast import Return
from tabnanny import check
from requests import post
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# from accounts.models import Post
from postsapi.models import Post
from .models import Like
from .service.post_service import PostService
from .serializers import LikeSerializer

"""
# class LikeView(APIView):
#  def post(self, request):
#       post_id = request.data.get('post_id')
#        if not post_id:
#             return Response({"error": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             post = Post.objects.get(id=post_id)
#         except Post.DoesNotExist:
#             return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the user already liked the post
#         like, created = Like.objects.get_or_create(
#             user=request.user, post=post)

#         if not created:
#             return Response({"error": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"like": LikeSerializer(like).data}, status=status.HTTP_201_CREATED)
"""

from .utils import LikeCache  # Import LikeCache class

# from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Like, Post
from .serializers import LikeSerializer

# from .cache import LikeCache  # Assuming you have this
from rest_framework.authentication import SessionAuthentication
from drf_spectacular.utils import extend_schema


class LikeViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: LikeSerializer},
        tags=["Likes"],
    )
    @action(
        detail=False,
        methods=["post"],
    )
    # def like_post(self, request):
    def post(self, request):
        """
        API to like a post.
        Expects a JSON body with a "post_id" field.
        Returns the created like object and the updated likes count.
        """
        post_id = request.data.get("post_id")
        if not post_id:
            return Response(
                {"error": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"error": "You already liked this post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        LikeCache.update_likes_cache(post.id)
        likes_count = LikeCache.get_cached_likes_count(post.id)

        return Response(
            {"like": LikeSerializer(like).data, "likes_count": likes_count},
            status=status.HTTP_201_CREATED,
        )


class LikeDeleteViewSet(ViewSet):
    """
    ViewSet to handle liking and unliking posts.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def destroy(self, request, pk=None):
        """
        API to unlike a post (delete like).
        """
        try:
            like = get_object_or_404(Like, id=pk)
            like_data = {
                "id": like.id,
                "post_id": like.post_id,
                "user_id": like.user_id,
            }
            post_id = like.post.id
            like.delete()
            LikeCache.invalidate_cache(post_id)
            likes_count = LikeCache.get_cached_likes_count(post_id)
            return Response(
                {"like": like_data, "likes_count": likes_count, "success": "OK"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"like": like_data, "success": "OK"}, status=status.HTTP_200_OK)
