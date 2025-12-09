from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Offer, Skill, Profile, SwapProposal, Message, Request
from .forms import OfferForm, ProposeForm, MessageForm, SignUpForm, RequestForm, OTPTokenForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def index(request):

    offers = Offer.objects.order_by('-created_at')[:12]
    suggestions = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        suggestions = find_matches(profile)[:6]
    return render(request, 'skilloryx/index.html', {'offers':offers, 'suggestions':suggestions})

def offer_list(request):
    q = request.GET.get('q','')
    if q:
        offers = Offer.objects.filter(skill__name__icontains=q)
    else:
        offers = Offer.objects.order_by('-created_at')
    return render(request, 'skilloryx/offer_list.html', {'offers':offers, 'q':q})

def offer_detail(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    return render(request, 'skilloryx/offer_detail.html', {'offer':offer})

@login_required
def offer_create(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.profile = profile
            offer.save()
            return redirect('offers')
    else:
        form = OfferForm()
    return render(request, 'skilloryx/offer_form.html', {'form':form})

@login_required
def offer_delete(request, pk):
    offer = get_object_or_404(Offer, pk=pk, profile__user=request.user)
    offer.delete()
    return redirect('profile', username=request.user.username)

@login_required
def request_create(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.profile = profile
            request_obj.save()
            return redirect('profile', username=request.user.username)
    else:
        form = RequestForm()
    return render(request, 'skilloryx/request_form.html', {'form': form})

@login_required
def propose_swap(request, offer_id):
    profile, created = Profile.objects.get_or_create(user=request.user)
    target = get_object_or_404(Offer, id=offer_id)
    if target.profile == profile:
        return redirect('offer_detail', pk=offer_id)
    if request.method == 'POST':
        our_offer_id = request.POST.get('our_offer')
        our_offer = get_object_or_404(Offer, id=our_offer_id, profile=profile)
        proposal = SwapProposal.objects.create(
            proposer=profile,
            responder=target.profile,
            offer_from_proposer=our_offer,
            offer_from_responder=target,
            message=request.POST.get('message','')
        )
        return redirect('proposals')
    else:
        my_offers = profile.offers.all()
        return render(request, 'skilloryx/propose.html', {'target':target, 'my_offers':my_offers})

@login_required
def proposal_list(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    sent = profile.proposals_sent.all()
    received = profile.proposals_received.all()
    return render(request, 'skilloryx/proposal_list.html', {'sent':sent, 'received':received})

@login_required
def proposal_detail(request, pk):
    profile, created = Profile.objects.get_or_create(user=request.user)
    proposal = get_object_or_404(SwapProposal, pk=pk)
    if profile not in [proposal.proposer, proposal.responder]:
        return redirect('index')
    message_form = MessageForm()
    return render(request, 'skilloryx/proposal_detail.html', {'proposal':proposal, 'message_form':message_form})

@login_required
def proposal_message(request, pk):
    profile, created = Profile.objects.get_or_create(user=request.user)
    proposal = get_object_or_404(SwapProposal, pk=pk)
    if profile not in [proposal.proposer, proposal.responder]:
        return redirect('index')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.proposal = proposal
            msg.sender = profile
            msg.save()

            from django.http import JsonResponse
            return JsonResponse({'success':True, 'content':msg.content, 'created_at': str(msg.created_at), 'sender': msg.sender.user.username})
    from django.http import JsonResponse

    msgs = list(proposal.messages.values('id','sender__user__username','content','created_at'))
    return JsonResponse({'messages':msgs})

@login_required
def proposal_accept(request, pk):
    profile, created = Profile.objects.get_or_create(user=request.user)
    proposal = get_object_or_404(SwapProposal, pk=pk)
    if profile != proposal.responder:
        return redirect('index')
    proposal.status = 'accepted'
    proposal.save()

    # Send real-time notification to proposer
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'user_{proposal.proposer.user.username}',
        {
            'type': 'user_notification',
            'message': {
                'type': 'video_call_invitation',
                'proposal_id': pk,
                'message': f'{proposal.responder.user.username} has accepted your proposal. Join the video call now!',
                'url': request.build_absolute_uri(f'/video_call/{pk}')
            }
        }
    )

    # Send email notification to proposer
    subject = 'Your Swap Proposal Has Been Accepted!'
    message = f'''
Hello {proposal.proposer.user.username},

Your swap proposal for {proposal.offer_from_proposer.skill.name} has been accepted by {proposal.responder.user.username}.

You can now join the video call to discuss the details.

Click here to join: {request.build_absolute_uri('/video_call/' + str(pk))}

Best regards,
SkillOryx Team
'''
    send_mail(subject, message, None, [proposal.proposer.user.email])

    # Redirect to video call immediately
    return redirect('video_call', room_name=pk)

@login_required
def proposal_decline(request, pk):
    profile, created = Profile.objects.get_or_create(user=request.user)
    proposal = get_object_or_404(SwapProposal, pk=pk)
    if profile != proposal.responder:
        return redirect('index')
    proposal.status = 'declined'
    proposal.save()
    return redirect('proposal_detail', pk=pk)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create TOTP device for 2FA
            device = TOTPDevice.objects.create(user=user, name='default')
            # Don't login yet, redirect to 2FA setup
            request.session['setup_user_id'] = user.id
            return redirect('otp_setup')
    else:
        form = SignUpForm()
    return render(request, 'skilloryx/signup.html', {'form':form})

def otp_setup_view(request):
    user_id = request.session.get('setup_user_id')
    if not user_id:
        return redirect('signup')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('signup')

    device = TOTPDevice.objects.get(user=user, name='default')
    if request.method == 'POST':
        form = OTPTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            if device.verify_token(token):
                device.confirmed = True
                device.save()
                login(request, user)
                del request.session['setup_user_id']
                return redirect('index')
            else:
                form.add_error('token', 'Invalid token. Please try again.')
    else:
        form = OTPTokenForm()

    import qrcode
    import io
    import base64
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(device.config_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'skilloryx/otp_setup.html', {'form': form, 'qr_code': qr_code, 'device': device})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile, created = Profile.objects.get_or_create(user=user)
            if profile.is_2fa_enabled:
                # Redirect to OTP verification
                request.session['login_user_id'] = user.id
                return redirect('otp_verify')
            else:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'skilloryx/login.html', {'form': form})

def otp_verify_view(request):
    user_id = request.session.get('login_user_id')
    if not user_id:
        return redirect('login')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    devices = TOTPDevice.objects.filter(user=user, confirmed=True)
    if not devices:
        # No 2FA setup, proceed to login
        login(request, user)
        del request.session['login_user_id']
        return redirect('index')

    if request.method == 'POST':
        form = OTPTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            for device in devices:
                if device.verify_token(token):
                    login(request, user)
                    del request.session['login_user_id']
                    return redirect('index')
            form.add_error('token', 'Invalid token. Please try again.')
    else:
        form = OTPTokenForm()

    return render(request, 'skilloryx/otp_verify.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'skilloryx/profile_edit.html', {'form': form})

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    return render(request, 'skilloryx/profile.html', {'profile':profile})

def about_view(request):
    return render(request, 'skilloryx/about.html')

def privacy_view(request):
    return render(request, 'skilloryx/privacy.html')

def terms_view(request):
    return render(request, 'skilloryx/terms.html')

@login_required
def video_call(request, room_name):
    return render(request, 'skilloryx/video_call.html', {'room_name': room_name})

def contact_view(request):
    return render(request, 'skilloryx/contact.html')


def find_matches(profile):
    my_offers = set(o.skill for o in profile.offers.all())
    my_requests = set(r.skill for r in profile.requests.all())
    candidates = []
    for offer in Offer.objects.filter(skill__in=my_requests).exclude(profile=profile):
        other = offer.profile
        other_offers = set(o.skill for o in other.offers.all())
        other_requests = set(r.skill for r in other.requests.all())
        score = 0
        if any(skill in my_offers for skill in other_requests):
            score += 2
        if offer.available_online:
            score += 1
        if profile.location and profile.location == other.location:
            score += 1
        candidates.append((other, score, offer))
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates
