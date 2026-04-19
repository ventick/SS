from rest_framework import serializers

from .models import Membership, StudyGroup, Subject


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "name", "code"]


class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Membership
        fields = ["id", "user", "username", "joined_at"]


class StudyGroupSerializer(serializers.ModelSerializer):
    creator_name = serializers.ReadOnlyField(source="creator.username")
    subject_details = SubjectSerializer(source="subject", read_only=True)
    members = MembershipSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = StudyGroup
        fields = [
            "id",
            "title",
            "description",
            "subject",
            "subject_details",
            "creator",
            "creator_name",
            "max_members",
            "is_active",
            "created_at",
            "members",
            "member_count",
        ]
        read_only_fields = [
            "creator",
            "is_active",
            "members",
            "member_count",
            "created_at",
        ]

    def get_member_count(self, obj):
        return obj.members.count()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs


class RemoveMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
