from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Membership, StudyGroup, Subject
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    RemoveMemberSerializer,
    StudyGroupSerializer,
    SubjectSerializer,
)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
            },
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data["username"]
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(
        username=username,
        password=serializer.validated_data["password"],
    )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
            },
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def subject_list(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def join_group(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)

    if Membership.objects.filter(user=request.user, group=group).exists():
        return Response(
            {"error": "You are already a member of this group."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if group.members.count() >= group.max_members:
        return Response(
            {"error": "This group is already full."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    Membership.objects.create(user=request.user, group=group)
    serializer = StudyGroupSerializer(group)
    return Response(
        {
            "message": "You joined the group successfully.",
            "group": serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def leave_group(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)
    membership = Membership.objects.filter(user=request.user, group=group).first()

    if not membership:
        return Response(
            {"error": "You are not a member of this group."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    membership.delete()
    serializer = StudyGroupSerializer(group)
    return Response(
        {
            "message": "You left the group successfully.",
            "group": serializer.data,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def remove_member(request, pk):
    group = get_object_or_404(StudyGroup, pk=pk)

    if group.creator != request.user:
        return Response(
            {"error": "Only the group creator can remove members."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = RemoveMemberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data["user_id"]
    if user_id == request.user.id:
        return Response(
            {"error": "The creator cannot remove themselves."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    membership = Membership.objects.filter(user_id=user_id, group=group).first()
    if not membership:
        return Response(
            {"error": "User not found in this group."},
            status=status.HTTP_404_NOT_FOUND,
        )

    membership.delete()
    group_serializer = StudyGroupSerializer(group)
    return Response(
        {
            "message": "Member removed successfully.",
            "group": group_serializer.data,
        }
    )


class GroupListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        groups = StudyGroup.active_groups.all()
        serializer = StudyGroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudyGroupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(creator=request.user)
        Membership.objects.get_or_create(user=request.user, group=group)
        return Response(StudyGroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(StudyGroup, pk=pk)

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = StudyGroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        group = self.get_object(pk)
        if group.creator != request.user:
            return Response({"error": "Only creator can edit"}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudyGroupSerializer(group, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        group = self.get_object(pk)
        if group.creator != request.user:
            return Response({"error": "Only creator can delete"}, status=status.HTTP_403_FORBIDDEN)

        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
