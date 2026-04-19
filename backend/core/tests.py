from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Membership, StudyGroup, Subject


class GroupApiTests(APITestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username="creator", password="pass12345")
        self.member = User.objects.create_user(username="member", password="pass12345")
        self.subject = Subject.objects.create(name="Web Development", code="WD101")
        self.group = StudyGroup.objects.create(
            title="Algorithms Sprint",
            description="Midterm prep",
            subject=self.subject,
            creator=self.creator,
            max_members=3,
        )
        Membership.objects.create(user=self.creator, group=self.group)

    def test_login_returns_token_and_user_payload(self):
        response = self.client.post(
            reverse("login"),
            {"username": "creator", "password": "pass12345"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user"]["username"], "creator")

    def test_group_detail_includes_members_and_member_count(self):
        response = self.client.get(reverse("group-detail", args=[self.group.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["member_count"], 1)
        self.assertEqual(response.data["members"][0]["username"], "creator")

    def test_authenticated_user_can_join_group(self):
        refresh = RefreshToken.for_user(self.member)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        response = self.client.post(reverse("join-group", args=[self.group.id]), format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Membership.objects.filter(user=self.member, group=self.group).exists())
