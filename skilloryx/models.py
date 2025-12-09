from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_otp.plugins.otp_totp.models import TOTPDevice

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    @property
    def is_2fa_enabled(self):
        return TOTPDevice.objects.filter(user=self.user, confirmed=True).exists()

class Skill(models.Model):
    name = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.name

LEVEL_CHOICES = [
    ('beginner','Beginner'),
    ('intermediate','Intermediate'),
    ('expert','Expert'),
]

class Offer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='offers')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    available_online = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile','skill')

    def __str__(self):
        return f"{self.profile.user.username} offers {self.skill.name}"

class Request(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requests')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile','skill')

    def __str__(self):
        return f"{self.profile.user.username} requests {self.skill.name}"

class SwapProposal(models.Model):
    proposer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='proposals_sent')
    responder = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='proposals_received')
    offer_from_proposer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='+')
    offer_from_responder = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='+')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending','Pending'),
        ('accepted','Accepted'),
        ('declined','Declined'),
        ('completed','Completed')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal {self.id}: {self.proposer} -> {self.responder} ({self.status})"

class Message(models.Model):
    proposal = models.ForeignKey(SwapProposal, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Msg {self.id} by {self.sender}"

class Review(models.Model):
    swap = models.OneToOneField(SwapProposal, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews_made')
    rating = models.PositiveSmallIntegerField()  # 1-5
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
