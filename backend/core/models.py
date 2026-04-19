from django.contrib.auth.models import User
from django.db import models


class ActiveStudyGroupManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def with_available_slots(self):
        return self.get_queryset()


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    code = models.CharField(max_length=20, unique=True, verbose_name="Код предмета")

    def __str__(self):
        return f"{self.code} - {self.name}"


class StudyGroup(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="groups")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_groups")
    max_members = models.PositiveIntegerField(verbose_name="Лимит участников")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    active_groups = ActiveStudyGroupManager()

    def __str__(self):
        return self.title


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name="members")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "group")


class Category(models.Model):
    name = models.CharField(max_length=50)
    subjects = models.ManyToManyField(Subject, related_name="categories")

    def __str__(self):
        return self.name
