# SkillOryx - Skill Swapping Platform
#### Video Demo:  <URL HERE>
#### Description:

## 📋 Overview

**SkillOryx** is a modern, community-driven skill-swapping platform built with Django. It allows users to exchange their skills with others in their community without monetary transactions. Whether you want to learn guitar while teaching coding, or exchange photography lessons for French lessons, SkillOryx connects you with the right people.

## ✨ Features

### User Authentication & Profiles
- **User Registration & Login** - Secure account creation and authentication with 2FA
- **User Profiles** - Display skills offered, skills wanted to learn, and member statistics
- **Profile Customization** - Edit bio, location, and upload profile photo
- **Profile Management** - Full profile editing with photo upload support
- **Auto-Profile Creation** - Profiles automatically created when users sign up

### Skill Offers & Requests
- **Create Offers** - Share skills you want to teach with difficulty levels (Beginner, Intermediate, Advanced)
- **Browse Offers** - Discover skills offered by other community members
- **Search & Filter** - Find offers by skill name and availability (online/in-person)
- **Skill Management** - Create, view, delete, and manage your skill offerings
- **Add Skills to Learn** - Specify skills you want to acquire from others
- **Online Availability** - Mark skills as available online or in-person only

### Skill Swapping (Proposals)
- **Propose Swaps** - Send proposals to swap your skill for someone else's
- **View Proposals** - See both sent and received proposals
- **Proposal Status Tracking** - Monitor proposal status (Pending, Accepted, Declined, Completed)
- **Proposal Management** - Accept, decline, or reject previously accepted proposals
- **Real-time Messaging** - Chat with the other person during a swap negotiation
- **Accept/Decline** - Respond to incoming swap proposals

### User Experience
- **Dark Theme UI** - Modern, eye-friendly dark mode design
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile
- **Real-time Notifications** - See proposal updates instantly
- **Color-coded Status Badges** - Quick visual feedback on proposal status

## 🛠️ Technology Stack

### Backend
- **Django 6.0** - Python web framework
- **Django ORM** - Database abstraction layer
- **SQLite3** - Development database

### Frontend
- **Bootstrap 5.3** - Responsive CSS framework
- **Font Awesome 6.4** - Icon library
- **Vanilla JavaScript** - Dynamic messaging and interactions
- **HTML5 & CSS3** - Semantic markup and modern styling

### Key Libraries
- `django-select2` - Enhanced dropdown selection
- `Pillow` - Image handling for avatars

## 📁 Project Structure

```
project/main/
├── manage.py                       # Django management script
├── db.sqlite3                      # Development database
├── render.yaml                     # Render deployment configuration
├── requirements.txt                # Python dependencies
├── main/                           # Main project settings
│   ├── __init__.py                 # Package initialization
│   ├── settings.py                 # Django configuration
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py                     # WSGI application
│   └── asgi.py                     # ASGI application for WebSockets
├── skilloryx/                      # Main app
│   ├── __init__.py                 # Package initialization
│   ├── models.py                   # Database models
│   ├── views.py                    # View functions
│   ├── urls.py                     # App URL routing
│   ├── forms.py                    # Django forms
│   ├── admin.py                    # Django admin config
│   ├── apps.py                     # App configuration
│   ├── consumers.py                # WebSocket consumers
│   ├── routing.py                  # WebSocket routing
│   ├── signals.py                  # Signal handlers
│   ├── tests.py                    # Unit tests
│   └── migrations/                 # Database migrations
├── templates/skilloryx/            # HTML templates
│   ├── about.html                  # About page
│   ├── base.html                   # Base template (navbar, footer)
│   ├── contact.html                # Contact page
│   ├── index.html                  # Homepage
│   ├── login.html                  # Login page
│   ├── offer_detail.html           # Single offer details
│   ├── offer_form.html             # Create new offer
│   ├── offer_list.html             # Browse all offers
│   ├── otp_setup.html              # 2FA setup page
│   ├── otp_verify.html             # 2FA verification page
│   ├── privacy.html                # Privacy policy page
│   ├── profile.html                # User profile display
│   ├── profile_edit.html           # Profile editing form
│   ├── proposal_detail.html        # Proposal details + messaging
│   ├── proposal_list.html          # View proposals (sent/received)
│   ├── propose.html                # Propose a swap
│   ├── request_form.html           # Add skill to learn
│   ├── signup.html                 # Registration page
│   ├── terms.html                  # Terms of service page
│   └── video_call.html             # Video call interface
├── static/                         # Source static assets
│   └── css/skilloryx.css           # Custom styles
└── staticfiles/                    # Collected static files
    ├── admin/                      # Django admin static files
    └── css/skilloryx.css           # Compiled custom styles
```

## 🗄️ Database Models

### Profile
- **User** (OneToOneField to Django User)
- **Bio** - Text description
- **Location** - Geographic location
- **Photo** - Profile image upload

### Skill
- **Name** - Skill name (e.g., "Python Programming", "Guitar")
- **Description** - Optional skill details

### Offer
- **Profile** (ForeignKey) - Who's offering the skill
- **Skill** (ForeignKey) - Which skill
- **Level** - Difficulty (beginner, intermediate, advanced)
- **Description** - Details about the skill
- **Available Online** - Boolean flag
- **Created At / Updated At** - Timestamps

### Request
- **Profile** (ForeignKey) - Who wants to learn
- **Skill** (ForeignKey) - What they want
- **Details** - Specific requirements

### SwapProposal
- **Proposer** (ForeignKey) - Who's proposing
- **Responder** (ForeignKey) - Who's receiving proposal
- **Offer From Proposer** (ForeignKey) - What proposer offers
- **Offer From Responder** (ForeignKey) - What responder offers
- **Message** - Initial proposal message
- **Status** - pending, accepted, declined, completed

### Message
- **Proposal** (ForeignKey) - Which swap it's about
- **Sender** (ForeignKey to Profile) - Who sent it
- **Content** - Message text

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
   ```bash
   cd /workspaces/127124566/project/main
   ```

2. **Install dependencies**
   ```bash
   pip install django pillow
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (admin account)
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver 0.0.0.0:8001
   ```

6. **Open in browser**
   ```bash
   "$BROWSER" http://127.0.0.1:8001
   ```

## 📖 Usage Guide

### For Users

#### 1. Sign Up
- Click **Sign Up** on the homepage
- Enter username, email, and password
- Your profile is automatically created

#### 2. Edit Your Profile
- Go to your profile via the **Profile** link
- Click **Edit** to update your bio, location, and upload a profile photo
- Click **Save Changes** to update your profile

#### 3. Create an Offer
- Go to **Create Offer** in the navbar
- Select a skill or type a new one
- Set difficulty level
- Add description of what you teach
- Mark if available online
- Click **Create Offer**

#### 4. Browse Skills
- Visit **Offers** page to see all available skills
- Click **View Details** on any offer
- View the person's profile

#### 5. Propose a Swap
- On an offer detail page, click **Propose Swap**
- Select one of your skills to exchange
- Add a message explaining your interest
- Click **Send Proposal**

#### 6. Manage Proposals
- Go to **My Proposals** in the navbar
- See proposals you've sent and received
- Click on a proposal to view details and chat
- Accept or decline proposals

### For Admins

1. **Access Admin Panel**
   ```
   http://127.0.0.1:8001/admin
   ```

2. **Manage Users, Offers, Proposals, and Skills**

## 🎨 Design Features

### Color Scheme
- **Primary Dark** (#1a1a2e) - Main background
- **Highlight** (#e94560) - Call-to-action (pink)
- **Success** (#00d4aa) - Positive actions (teal)
- **Text Light** (#eaeaea) - Main text

### UI Components
- Responsive navbar with sticky positioning
- Card-based layout for organized content
- Gradient headers and visual dividers
- Color-coded status badges
- Real-time messaging system

## 🚨 Troubleshooting

### Profile doesn't exist for user
```bash
python manage.py shell
from django.contrib.auth.models import User
from skilloryx.models import Profile
for user in User.objects.all():
    Profile.objects.get_or_create(user=user)
exit()
```

### Reset database
```bash
rm db.sqlite3
rm -rf skilloryx/migrations/*
touch skilloryx/migrations/__init__.py
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Testing

Run unit tests:
```bash
python manage.py test skilloryx
```

## 📈 Future Enhancements

- Rating system for users
- Skill categories and advanced search
- Email/push notifications
- ML-based skill recommendations
- Mobile app versions
- Video conferencing integration
- Calendar scheduling
- Payment system for premium features
- Community forums

## 📄 License

MIT License - Open source and free to use

## 👥 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions, open an issue on GitHub or contact asifhasan10122000@gmail.com

---

**Happy Skill Swapping! 🎓✨**

Last Updated: December 2025
