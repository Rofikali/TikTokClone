import re
import stat
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from requests import session
from postsapi.serializers import PostSerializer
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from postsapi.models import Post
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.schemas.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from django.middleware.csrf import get_token
from .serializers import UserSerializer
from .serializers import (
    LoginSerializer,
    # AllPostsSerializer,
    UpdateUserImageSerializer,
    UserRegistrationSerializer,
    UsersCollectionSerializer,
    UserSerializer,
)
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.contrib.auth import logout
# import response

User = get_user_model()
# from .models import Post, User, Comment, Like, Post
from django.core.files.storage import default_storage

# from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# drf spectacular schema
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .services import FileService

# rewrite this code to use the CSRF token in the header using viewsets


class CSRFTokenViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    """
    Provides a CSRF token to the client as a cookie.
    """

    @extend_schema(
        tags=["accounts"],
    )
    def list(self, request, *args, **kwargs):
        csrf_token = get_token(request)  # Generate or retrieve CSRF token
        response = JsonResponse({"detail": "CSRF cookie set"})
        # Optional: Include token in response header
        response["X-CSRFToken"] = csrf_token
        # return response
        return Response(
            {"detail": "CSRF cookie set", "csrfToken": csrf_token},
            status=status.HTTP_200_OK,
        )


class RegisterUserViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    @extend_schema(
        # This links the serializer for the request body
        request=UserRegistrationSerializer,
        responses={
            201: UserRegistrationSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
    def create(self, request):
        """
        Registering a user

        """
        serializer = UserRegistrationSerializer(data=request.data)
        print("serializer ---->", serializer)
        print("request.data ---->", request.data)

        if serializer.is_valid():
            try:
                # Create the user
                user = serializer.save()
                print("user ---->", user)

                # Optionally create a token
                token = Token.objects.create(user=user)
                print("token ---->", token)
                # send email verification

                # return Response(
                #     {
                #         "token": token.key,
                #     },
                #     status=status.HTTP_201_CREATED,
                # )

                response = Response(
                    {
                        "token": token.key,
                        "success": f"You {request.user.username} or successfully registered !!",
                        "status": status.HTTP_201_CREATED,
                    }
                )
                return response
            except InterruptedError:
                return Response(
                    {"error": "A user with this email or username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = [AllowAny]  # Disable permissions for this route

    @extend_schema(
        # This links the serializer for the request body
        request=LoginSerializer,
        responses={
            201: LoginSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
    def create(self, request):
        if self.is_rate_limited(request):
            raise ValidationError("Too many login attempts. Try again later.")

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # ✅ Set sessionid cookie

                return Response(
                    {"detail": "Login successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Invalid credentials"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def is_rate_limited(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        user_email = request.data.get("email")

        cache_key = f"login_attempt_{user_email}_{ip_address}"
        attempts = cache.get(cache_key, 0)

        if attempts >= 100:  # Limit to 10 attempts
            return True

        cache.set(cache_key, attempts + 1, timeout=60)  # 60 seconds timeout
        return False


class LoggedInUserViewSet(ViewSet):
    """
    API to get details of the logged-in user.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer},
        tags=["accounts"],
    )
    def list(self, request):
        print("🔍 [DEBUG] Incoming request to LoggedInUserViewSet.retrieve")

        # Authentication Info
        print(f"🔐 [DEBUG] Authenticated user: {request.user}")
        print(f"🔐 [DEBUG] Is user authenticated? {request.user.is_authenticated}")

        # Headers
        print("📦 [DEBUG] Request Headers:")
        for key, value in request.headers.items():
            print(f"   {key}: {value}")

        # Cookies
        print("🍪 [DEBUG] Request Cookies:")
        for key, value in request.COOKIES.items():
            print(f"   {key}: {value}")

        # Session
        print("📘 [DEBUG] Session Keys:")
        for key in request.session.keys():
            print(f"   {key}: {request.session.get(key)}")

        # Serialize and prepare response
        serializer = UserSerializer(request.user)
        csrf_token = get_token(request)
        session_id = request.COOKIES.get("sessionid", None)

        print("✅ [DEBUG] Serialized user data:", serializer.data)

        response = Response(
            {
                "debug": "No errors, user fetched",
                "user_data": serializer.data,
                "csrf_token": csrf_token,
                "sessionid": session_id,
            },
            status=status.HTTP_200_OK,
        )

        # Optionally also return CSRF token in headers (for frontend convenience)
        response.headers["X-CSRFToken"] = csrf_token

        return response


from django.shortcuts import get_object_or_404


class ProfileViewSet(ViewSet):
    authentication_classes = []  # Disable authentication for this route
    permission_classes = []  # Disable permissions for this route
    """
    API to display the user's posts and profile information.
    """

    @extend_schema(
        responses={200: UserSerializer},
        tags=["accounts"],
        description="Retrieve a user's profile and their posts.",
    )
    def retrieve(self, request, pk=None):
        """
        Retrieve a user's profile and their posts.
        """
        try:
            user = get_object_or_404(User, pk=pk)
            posts = Post.objects.filter(user=user).order_by("-created_at")

            # Serialize the data
            post_serializer = PostSerializer(
                posts, many=True, context={"request": request}
            )
            user_serializer = UserSerializer(user)

            return Response(
                {
                    "posts": post_serializer.data,
                    "user": user_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class LogoutViewSet(ViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={204: None},
        tags=["accounts"],
    )
    def create(self, request):
        print("🔍 [DEBUG] Incoming request to LogoutViewSet.create")
        print(f"🔐 [DEBUG] Authenticated user: {request.user}")
        print(f"🔐 [DEBUG] Is user authenticated? {request.user.is_authenticated}")

        # Log out the user by flushing the session
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class GetRandomUsersViewSet(ViewSet):
    @extend_schema(
        request=UserSerializer,  # This links the serializer for the request body
        responses={
            201: UserSerializer
        },  # Expected response will be the created category
        tags=["accounts"],
    )
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
