from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .serializers import (
    UserSerializer,
    UsersCollectionSerializer,
    PostSerializer,
    PostSerializer,
    # AllPostsSerializer,
    UpdateUserImageSerializer,
    CommentSerializer,
    PostSerializer,
    UserRegistrationSerializer,
)
from rest_framework import viewsets
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle
from .serializers import LoginSerializer
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from rest_framework.permissions import AllowAny
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Post, User, Post

# from .models import Post, User, Comment, Like, Post
from .services import FileService
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from django.contrib.auth.models import User
from .services import FileService  # Assuming FileService is implemented
from django.shortcuts import get_object_or_404, redirect

from pagination.custompagination import (
    CustomPageNumberPagination,
    CustomCursorPagination,
)


from rest_framework.viewsets import ViewSet
from rest_framework.response import Response


# rewrite this code to use the CSRF token in the header using viewsets
class CSRFTokenViewSet(ViewSet):
    """
    Provides a CSRF token to the client as a cookie.
    """

    authentication_classes = []  # Disable authentication for this route
    permission_classes = []  # Disable permissions for this route

    def list(self, request, *args, **kwargs):
        csrf_token = get_token(request)  # Generate or retrieve CSRF token
        response = JsonResponse({"detail": "CSRF cookie set"})
        # Optional: Include token in response header
        response["X-CSRFToken"] = csrf_token
        return response


class RegisterUserViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = []  # Disable permissions for this route

    def create(self, request):
        """
        Registering a user

        """
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            try:
                # Create the user
                user = serializer.save()

                # Optionally create a token
                token = Token.objects.create(user=user)

                return Response({"token": token.key}, status=status.HTTP_201_CREATED)
            except InterruptedError as e:
                return Response(
                    {"error": "A user with this email or username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
# class RegisterUserView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 # Create the user
#                 user = serializer.save()

#                 # Optionally create a token
#                 token = Token.objects.create(user=user)

#                 return Response({"token": token.key}, status=status.HTTP_201_CREATED)
#             except InterruptedError as e:
#                 return Response(
#                     {"error": "A user with this email or username already exists."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        if self.is_rate_limited(request):
            raise ValidationError("Too many login attempts. Try again later.")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)

            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_rate_limited(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        user_email = request.data.get("email")

        cache_key = f"login_attempt_{user_email}_{ip_address}"
        attempts = cache.get(cache_key, 0)

        if attempts >= 5:
            return True

        cache.set(cache_key, attempts + 1, timeout=60)  # 60 seconds timeout
        return False


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()  # Delete the token to log out
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
# class LoggedInUser(APIView):

#     """
#     API to get details of the logged-in user.
#     """

#     def get(self, request):
#         try:
#             user = request.user  # Get the logged-in user
#             serializer = UserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
'''


class LoggedInUser(APIView):
    """
    API to get details of the logged-in user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                return Response(
                    {"error": "User not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserImage(APIView):
    """
    API to update user image with validation and cropping dimensions.
    """

    def post(self, request):
        print("Received data:", request.data)  # Debugging
        # Check if the file is being sent correctly
        print("Files:", request.FILES)

        serializer = UpdateUserImageSerializer(data=request.data)
        if not serializer.is_valid():
            print("Validation errors:", serializer.errors)  # Debugging
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not all(key in request.data for key in ["height", "width", "top", "left"]):
            return Response(
                {"error": "The dimensions are incomplete"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = request.user
            print("user for update image  ")
            # Assuming the service handles image updates
            FileService.update_image(user, request.data)
            user.save()
            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    """
    API to get details of a user by ID.
    """

    def get(self, request, id):
        try:
            user = get_object_or_404(User, id=id)
            serializer = UserSerializer(user, context={"request": request})
            return Response(
                {"success": "OK", "user": serializer.data}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    """
    API to update the logged-in user's name and bio.
    """

    def patch(self, request):
        serializer = UserSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = request.user
            user.name = request.data.get("name", user.name)
            user.bio = request.data.get("bio", user.bio)
            user.save()
            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostCreateView(APIView):
    """
    API to create a new post with a video.
    """

    def post(self, request):
        data = request.data
        video = request.FILES.get("video")

        if not video or not video.name.endswith(".mp4"):
            return Response(
                {"error": "The video field is required and must be a valid MP4 file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "text" not in data:
            return Response(
                {"error": "The text field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post(user=request.user, text=data["text"])
            # FileService to handle video uploads
            post = FileService.add_video(post, video)
            post.save()

            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    """
    API to retrieve a specific post and related posts by the same user.
    """

    def get(self, request, id):
        try:
            post = get_object_or_404(Post, id=id)
            related_posts = Post.objects.filter(user=post.user).values_list(
                "id", flat=True
            )

            # post_serializer = AllPostsSerializer([post], many=True)
            post_serializer = PostSerializer(
                [post], many=True, context={"request": request}
            )
            # return Response({
            #     'post': post_serializer.data,
            #     'ids': list(related_posts)
            # }, status=status.HTTP_200_OK)

            return Response(
                {
                    # post_serializer.data,
                    "post": post_serializer.data,
                    "ids": list(related_posts),
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PostDeleteView(APIView):
    """
    API to delete a specific post along with its associated video file.
    """

    def delete(self, request, id):
        try:
            post = get_object_or_404(Post, id=id)
            if post.video and default_storage.exists(post.video.path):
                # Delete the video file
                default_storage.delete(post.video.path)
            post.delete()

            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# working with it


class HomeViewSet(ViewSet):
    # permission_classes = [AllowAny]
    # pagination_class = CustomCursorPagination

    def list(self, request):
        # queryset = Post.objects.all().order_by("-created_at")
        # serializer = PostSerializer(queryset, many=True, context={"request": request})
        # return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            queryset = Post.objects.all()
            serializer = PostSerializer(
                queryset, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


'''
# class HomeView(APIView):
#     permission_classes = [AllowAny]
#     pagination_class = CustomCursorPagination
#     # pagination_class = CustomPageNumberPagination

#     """
#     API to display all posts ordered by creation date.
#     """

#     def get(self, request):
#         try:
#             posts = Post.objects.all().order_by("-created_at")
#             serializer = PostSerializer(
#                 posts, many=True, context={"request": request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
'''


class ProfileView(APIView):
    """
    API to display the user's posts and profile information.
    """

    def get(self, request, id):
        try:
            # Fetch posts by the specified user
            posts = Post.objects.filter(user_id=id).order_by("-created_at")
            # Fetch the user information
            user = User.objects.get(id=id)

            # Serialize the data
            # post_serializer = PostSerializer(posts, many=True)
            post_serializer = PostSerializer(
                posts, many=True, context={"request": request}
            )
            user_serializer = UserSerializer(user)

            return Response(
                {"posts": post_serializer.data, "user": user_serializer.data},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetRandomUsersViewSet(ViewSet):
    """
    API to get random suggested and followed users.
    """

    def list(self, request):
        try:
            # Fetch random users for suggestions (limit to 5)
            suggested_users = User.objects.order_by("?")[:5]
            # Fetch random users for following (limit to 10)
            following_users = User.objects.order_by("?")[:10]

            # Serialize the data
            suggested_serializer = UserSerializer(suggested_users, many=True)
            following_serializer = UserSerializer(following_users, many=True)

            return Response(
                {
                    "suggested": suggested_serializer.data,
                    "following": following_serializer.data,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


'''

# class GlobalView(APIView):
#     permission_classes = [AllowAny]

#     """
#     API to get random suggested and followed users.
#     """

#     def get(self, request):
#         try:
#             # Fetch random users for suggestions (limit to 5)
#             suggested_users = User.objects.order_by("?")[:5]
#             # Fetch random users for following (limit to 10)
#             following_users = User.objects.order_by("?")[:10]

#             # Serialize the data
#             suggested_serializer = UserSerializer(suggested_users, many=True)
#             following_serializer = UserSerializer(following_users, many=True)

#             return Response(
#                 {
#                     "suggested": suggested_serializer.data,
#                     "following": following_serializer.data,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
'''


class SendVerificationEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response(
                {"status": "email-already-verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Generate email verification token
        uid = urlsafe_base64_encode(user.pk.encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate verification link
        verification_link = f"http://{get_current_site(request).domain}{
            reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send verification email
        send_mail(
            "Email Verification",
            f"Please verify your email using this link: {verification_link}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response({"status": "verification-link-sent"}, status=status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode("utf-8")
            user = User.objects.get(pk=uid)

            # Check if the token is valid
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"status": "email-verified"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"status": "invalid-token"}, status=status.HTTP_400_BAD_REQUEST
                )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"status": "invalid-link"}, status=status.HTTP_400_BAD_REQUEST
            )


class RequestPasswordReset(APIView):
    """
    API to send a password reset email.
    """

    def post(self, request):
        email = request.data.get("email")

        # Check if email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate the password reset token
        uid = urlsafe_base64_encode(str(user.pk).encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate the reset password link
        reset_password_link = f"http://{get_current_site(request).domain}{
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send the reset email
        send_mail(
            "Password Reset Request",
            f"You can reset your password using the following link: {
                reset_password_link
            }",
            "from@example.com",
            [email],
            fail_silently=False,
        )

        return Response({"status": "reset-link-sent"}, status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def post(self, request, uidb64, token):
        # Validate the request data
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")

        if password != password_confirmation:
            raise ValidationError({"password": "Passwords do not match"})

        try:
            # Decode the UID
            uid = urlsafe_base64_decode(uidb64).decode("utf-8")
            user = User.objects.get(pk=uid)

            # Check if the token is valid
            if not default_token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Update the password
            user.set_password(password)
            user.save()

            return Response(
                {"status": "password reset successful"}, status=status.HTTP_200_OK
            )

        except (User.DoesNotExist, ValueError, OverflowError):
            return Response(
                {"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetLinkController(APIView):
    def post(self, request):
        email = request.data.get("email")

        # Validate email
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No user found with this email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate the password reset token
        uid = urlsafe_base64_encode(user.pk.encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate the password reset URL
        reset_url = f"http://{get_current_site(request).domain}{
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send email with the password reset link
        send_mail(
            "Password Reset Request",
            f"Use the following link to reset your password: {reset_url}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"status": "password reset link sent"}, status=status.HTTP_200_OK
        )


class VerifyEmailView(APIView):
    def get(self, request, uidb64, token):
        try:
            # Decode the user ID
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(id=uid)

            # Check the token
            if default_token_generator.check_token(user, token):
                if not user.email_verified:
                    user.email_verified = True
                    user.save()

                    # Optionally, you can log the user in after email verification
                    login(request, user)

                    # Return a success response
                    return Response(
                        {"message": "Email successfully verified."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"message": "Email already verified."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"message": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST,
            )


def send_verification_email(user):
    uid = urlsafe_base64_encode(str(user.id).encode())
    token = default_token_generator.make_token(user)
    verification_url = f"{settings.FRONTEND_URL}/verify-email/{uid}/{token}/"

    email_subject = "Verify your email address"
    email_message = render_to_string(
        "email/verify_email.html",
        {
            "user": user,
            "verification_url": verification_url,
        },
    )
    send_mail(email_subject, email_message, settings.DEFAULT_FROM_EMAIL, [user.email])


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    # You can use UsersCollectionSerializer for list representation
    def get_serializer_class(self):
        if self.action == "list":
            return UsersCollectionSerializer
        return UserSerializer
