from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Skill, Offer

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_profile_created(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)

class SkillTestCase(TestCase):
    def test_skill_creation(self):
        skill = Skill.objects.create(name='Python')
        self.assertEqual(skill.name, 'Python')

class OfferTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.skill = Skill.objects.create(name='Python')

    def test_offer_creation(self):
        offer = Offer.objects.create(
            profile=self.user.profile,
            skill=self.skill,
            level='beginner'
        )
        self.assertEqual(offer.profile.user, self.user)
