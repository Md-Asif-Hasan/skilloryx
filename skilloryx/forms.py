from django import forms
from .models import Offer, Request, SwapProposal, Message, Skill, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OfferForm(forms.ModelForm):
    # Turn Skill into a simple text input
    skill = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skill name'
        })
    )

    class Meta:
        model = Offer
        fields = ['skill', 'description', 'level', 'available_online']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'level': forms.Select(),
            'available_online': forms.CheckboxInput(),  # FIXED
        }

    def clean_skill(self):
        """
        Convert user-typed text into a Skill object.
        """
        skill_name = self.cleaned_data.get('skill').strip()

        if not skill_name:
            raise forms.ValidationError("Skill name cannot be empty.")

        # Get or create the Skill instance
        skill_obj, created = Skill.objects.get_or_create(
            name__iexact=skill_name,
            defaults={'name': skill_name}
        )
        return skill_obj

    def save(self, commit=True):
        """
        Save Offer with the actual Skill object.
        """
        instance = super().save(commit=False)
        instance.skill = self.cleaned_data['skill']  # Already a Skill object

        if commit:
            instance.save()

        return instance


class RequestForm(forms.ModelForm):
    skill = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skill name'
        })
    )

    class Meta:
        model = Request
        fields = ['skill', 'details']
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_skill(self):
        skill_name = self.cleaned_data.get('skill').strip()
        if not skill_name:
            raise forms.ValidationError("Skill name cannot be empty.")
        skill_obj, created = Skill.objects.get_or_create(
            name__iexact=skill_name,
            defaults={'name': skill_name}
        )
        return skill_obj

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.skill = self.cleaned_data['skill']
        if commit:
            instance.save()
        return instance

class ProposeForm(forms.ModelForm):
    class Meta:
        model = SwapProposal
        fields = ['message']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class OTPTokenForm(forms.Form):
    token = forms.CharField(max_length=6, label='Enter 6-digit code from your authenticator app')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
