from django.contrib import admin
from .models import Profile, Skill, Offer, Request, SwapProposal, Message, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Offer)
admin.site.register(Request)
admin.site.register(SwapProposal)
admin.site.register(Message)
admin.site.register(Review)
