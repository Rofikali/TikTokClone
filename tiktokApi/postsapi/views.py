from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema
from .models import Post
from .serializers import PostSerializer


class HomeViewSet(ViewSet):
    @extend_schema(
        request=PostSerializer,  # This links the serializer for the request body
        responses={
            200: PostSerializer,  # This links the serializer for the response
        },  # Expected response will be the created category
        tags=["Posts"],
        summary="list all posts",
        description="This endpoint allows you to list all posts.",
    )
    def list(self, request):
        try:
            queryset = Post.objects.all()
            serializer = PostSerializer(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error is here ": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


from django.shortcuts import get_object_or_404


class PostViewSets(ViewSet):
    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        tags=["Posts"],
        summary="Single post retrieve",
        description="This endpoint allows you to retrieve a single post.",
    )
    def retrieve(self, request, pk=None):
        try:
            post = get_object_or_404(Post, id=pk)

            # related_posts = Post.objects.filter(user=post.user).values()
            related_posts_ids = Post.objects.filter(user=post.user).values_list(
                "id", flat=True
            )

            post_serializer = PostSerializer(
                [post], many=True, context={"request": request}
            )

            return Response(
                {"post": post_serializer.data, "ids": list(related_posts_ids)},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class PostViewSets(ViewSet):
#     @extend_schema(
#         request=PostSerializer,  # This links the serializer for the request body
#         responses={
#             200: PostSerializer,  # This links the serializer for the response
#         },  # Expected response will be the created category
#         tags=["Posts"],
#         summary="Single post retrieve",
#         # path="posts/<int:pk>/",
#         description="This endpoint allows you to retrieve a single post.",
#     )
#     def retrieve(self, request, pk=None):
#         try:
#             post = get_object_or_404(Post, id=pk)  # noqa: F821
#             # related_posts = Post.objects.filter(user=post.user).values_list(
#             #     "id", flat=True
#             # )
#             related_posts = Post.objects.filter(user=post.user).values())  # noqa: F821
#             #     "id",
#             #     "text",
#             #     "video",
#             #     "created_at",
#             #     "user__id",
#             #     "user__name",
#             #     "user__email",
#             #     "user__image",
#             #     # "user__image"
#             #     # "user__image", "user__name"
#             #     # "user__email"
#             # )
#             print("related_posts", related_posts)
#             related_posts_data = Post.objects.filter(user=post.user).values_list(
#                 "id", flat=True
#             )
#             print("related_posts_data", related_posts_data)
#             # related_posts = related_posts_data  # noqa: F841

#             # post_serializer = AllPostsSerializer([post], many=True)
#             post_serializer = PostSerializer(
#                 [post], many=True, context={"request": request}
#             )
#             return Response(
#                 {"post": post_serializer.data, "ids": list(related_posts)},
#                 status=status.HTTP_200_OK,
#             )

#             return Response(
#                 {
#                     # post_serializer.data,
#                     "post": post_serializer.data,
#                     "ids": list(related_posts),
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     # def retrieve(self, request, pk=None):
#     #     try:
#     #         queryset = Post.objects.filter(id=pk)
#     #         if not queryset.exists():
#     #             return Response(
#     #                 {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
#     #             )
#     #         serializer = PostSerializer(
#     #             queryset, many=True, context={"request": request}
#     #         )
#     #         return Response(serializer.data, status=status.HTTP_200_OK)
#     #     except Exception as e:
#     #         return Response(
#     #             {"error is here ": str(e)}, status=status.HTTP_400_BAD_REQUEST
#     #         )


# class PostDetailView(APIView):
#     """
#     API to retrieve a specific post and related posts by the same user.
#     """

#     def get(self, request, id):
#         try:
#             post = get_object_or_404(Post, id=id)
#             related_posts = Post.objects.filter(user=post.user).values_list(
#                 "id", flat=True
#             )

#             # post_serializer = AllPostsSerializer([post], many=True)
#             post_serializer = PostSerializer(
#                 [post], many=True, context={"request": request}
#             )
#             # return Response({
#             #     'post': post_serializer.data,
#             #     'ids': list(related_posts)
#             # }, status=status.HTTP_200_OK)

#             return Response(
#                 {
#                     # post_serializer.data,
#                     "post": post_serializer.data,
#                     "ids": list(related_posts),
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(ViewSet):
    @extend_schema(
        request=PostSerializer,  # This links the serializer for the request body
        responses={
            200: PostSerializer,  # This links the serializer for the response
        },  # Expected response will be the created category
        tags=["Posts"],
        summary="Create a new post",
        description="This endpoint allows you to create a new post.",
    )
    def create(self, request):
        serializer = PostSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
