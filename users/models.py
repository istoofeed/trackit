import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    ROLE_CHOICES = (
        ("project manager", "Project Manager"),
        ("lead developer", "Lead Developer"),
        ("ui/ux designer", "UI/UX Designer"),
        ("qa tester", "QA Tester"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    email = models.EmailField(unique=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=255, blank=True)
    user_role = models.CharField(
        max_length=255, null=True, blank=True, choices=ROLE_CHOICES
    )
    specialized_in = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True, default="avatar.svg")
    in_group = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)
    chapters = models.ManyToManyField("Chapter")
    is_approved = models.BooleanField(default=False)
    # ! - Add more fields here

    def __str__(self):
        return self.name


@receiver(post_save, sender=Group)
def assign_chapters(sender, instance, created, **kwargs):
    if created:
        chapter1 = Chapter.objects.create(name="Chapter 1")
        chapter2 = Chapter.objects.create(name="Chapter 2")
        chapter3 = Chapter.objects.create(name="Chapter 3")
        chapter4 = Chapter.objects.create(name="Chapter 4")
        chapter5 = Chapter.objects.create(name="Chapter 5")
        section_names_ch1 = [
            "Introduction",
            "Background of the Study",
            "Statement of the Problem",
            "Project Context",
            "Purpose and Description",
            "General Objectives",
            "Specific Objectives",
            "Scope and Limitation",
            "Significance of the Study",
            "Definition of Terms",
        ]

        section_names_ch2 = [
            "Related Studies",
            "Related System",
            "Technical Background",
            "Synthesis Matrix",
        ]

        section_names_ch3 = [
            "Research Design",
            "Respondents of the study",
            "Population",
            "Sample",
            "Locale of the study",
            "Data Gathering Tools",
            "Data Gathering Procedures",
            "Data Analysis",
            "System Architecture",
            "Methodology",
            "Schedule and Timeline",
            "Budget Plan",
            "Project Team and Responsibilities",
            "Verification, Validation and Testing Plan",
            "Hierarchical Input Process Output",
            "Graphical User Interface and Functions",
        ]

        section_names_ch4 = [
            "Use Case Diagram",
            "Calendar of Activities",
            "Testing Plan",
            "Usability Testing",
        ]

        section_names_ch5 = [
            "Implementation Results",
            "Usability Test Results",
            "Discussions of Results",
            "Conclusion",
            "Recommendations",
        ]

        for name in section_names_ch1:
            section = Section.objects.create(name=name, chapter=chapter1)
            chapter1.save()

        for name in section_names_ch2:
            section = Section.objects.create(name=name, chapter=chapter2)
            chapter2.save()

        for name in section_names_ch3:
            section = Section.objects.create(name=name, chapter=chapter3)
            chapter3.save()

        for name in section_names_ch4:
            section = Section.objects.create(name=name, chapter=chapter4)
            chapter4.save()

        for name in section_names_ch5:
            section = Section.objects.create(name=name, chapter=chapter5)
            chapter5.save()

        instance.chapters.add(chapter1, chapter2, chapter3, chapter4, chapter5)


class Section(models.Model):
    chapter = models.ForeignKey(
        "Chapter",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sections",
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    date_finished = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]


class Chapter(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    date_started = models.DateTimeField(null=True, blank=True)
    date_ended = models.DateTimeField(null=True, blank=True)

    total_section = models.IntegerField(null=True, blank=True, default=0)
    chapter_progress = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    # @property
    # def getProgress(self):
    #     sections = self.sections.all()
    #     totalSection = sections.count()

    #     sectionFinished = sections.filter(is_done=True).count()

    #     progress = (sectionFinished / totalSection) * 100

    #     self.total_section = totalSection
    #     self.chapter_progress = progress
    #     self.is_done = progress == 100

    # def save(self, *args, **kwargs):
    #     self.getProgress()
    #     super().save(*args, **kwargs)
