# LoveLink — Interactive Digital Love Letter & Message Builder

> An emotionally captivating web platform where users can create personalized, beautiful, interactive digital experiences for their loved ones and share them via WhatsApp, Instagram, email, or direct secret URLs.

---

## 🌟 Key Features

### 1. 💌 3D Animated Envelope & Wax Seal Unboxing
- Recipients open an enchanting 3D envelope with custom wax seal stamping (*"BE MINE"*, *"LOVE"*, *"SORRY"*, *"ALWAYS"*).
- Breaking seal animation, sliding love letter peek, and page transition effects.
- Dynamic floating hearts particle engine and built-in romantic ambient audio chimes.

### 2. 💖 Interactive YES / NO Decision Engine
- Creators add proposals (*"Will you be my Valentine? ❤️"*, *"Can we go on a date this weekend?"*, *"Will you forgive me?"*).
- **YES Reaction**: Screen-wide celebratory confetti fireworks, personalized celebration message, and optional sweet reply note.
- **NO Reaction**: Respectful, caring response without forcing the recipient to change their answer.
- Anti-duplicate submission protection with optional answer revision.

### 3. 📧 Automated Transactional Email Alerts
- Triggers an instant email alert directly to the creator's verified email account the second a recipient answers.
- Strict security: recipient-supplied emails are never trusted; notifications only go to the verified experience owner.
- Notification history and preference toggles (*email_on_response*) in the creator dashboard.

### 4. 🎨 No-Code Visual Studio & Drag-and-Drop Editor
- **Multi-page experiences** with page reordering and custom transition effects.
- **Content Blocks**:
  - Animated 3D Envelopes
  - Romantic Titles & Subtitles
  - Love Letter Paragraphs (Classic Serif, Handwritten Cursive, Clean Sans)
  - Tilted Polaroid Photo Scrapbook with tape and captions
  - Interactive YES/NO Question Modules
  - Countdown Timers (Days, Hours, Minutes, Seconds)
  - Sign-off & Cursive Signatures
- Live Desktop vs Mobile phone frame preview toggles.

### 5. 🔒 Password-Protected Secret Access
- Optional Argon2 password hashing on private experiences.
- Rate-limited passkey gateway before any private photographs or notes are revealed.
- Generic metadata prevents link preview leaks on WhatsApp or Instagram.

### 6. 📱 Omnichannel Sharing & QR Codes
- One-click WhatsApp sharing with customizable message teaser.
- Instant QR Code generator for printed cards, physical gifts, or date surprises.
- Native mobile sharing and instant link copy.

### 7. 🖼️ Safe Media Management
- Upload personal photos with automatic thumbnail generation (Pillow).
- MIME-type validation, size verification (max 10MB), and per-user storage quotas (50MB).

### 8. 🛡️ Staff Admin & Moderation Portal
- Platform health metrics (total creators, experiences, visits, responses).
- One-click takedown and abuse report review system.

---

## 🏗️ System Architecture

```
Client (React + Vite + Tailwind/Romantic CSS)
   │
   ├─► Public Recipient Experience: /l/:slug (Wax seal envelope, floating hearts, YES/NO fireworks)
   ├─► Creator Studio: /editor/:id (Multi-page block editor, mobile/desktop split preview)
   ├─► Template Marketplace: /templates (Filterable categories, 1-click clone)
   └─► Dashboard & Analytics: /dashboard (Visits, responses, media manager, settings)
   │
   ▼ REST API (/api/v1/)
Backend (Django REST Framework + Argon2 + Pillow)
   │
   ├─► accounts (Token/Session Auth, registration, profiles)
   ├─► templates_gallery (Categories, seed templates, deep-cloning)
   ├─► experiences (Pages, blocks, access settings, secret slugs, analytics)
   ├─► interactions (YES/NO questions, options, response tracking)
   ├─► notifications (Email dispatch, preferences, audit log)
   ├─► media_assets (Image uploads, Lanczos thumbnails, quotas)
   └─► moderation (Abuse reports, staff takedown)
   │
   ▼
Database (PostgreSQL / SQLite)
```

---

## 🚀 Quickstart & Local Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ & npm

### 1. Backend Setup (Django)

```bash
cd backend

# Create & activate virtual environment (Windows PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed romantic templates and default admin account
python manage.py seed_templates
python manage.py init_admin

# Start Django development server (Port 8000)
python manage.py runserver 127.0.0.1:8000
```

*Default Administrator Account:*
- **Email:** `admin@lovelink.app`
- **Password:** `AdminLove2026!`

---

### 2. Frontend Setup (React + Vite)

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Start Vite dev server (Port 5173)
npm run dev
```

Open your browser to:
- **Web Platform:** [http://127.0.0.1:5173/](http://127.0.0.1:5173/)
- **Template Gallery:** [http://127.0.0.1:5173/templates](http://127.0.0.1:5173/templates)
- **Creator Dashboard:** [http://127.0.0.1:5173/dashboard](http://127.0.0.1:5173/dashboard)
- **Backend API Root:** [http://127.0.0.1:8000/api/v1/](http://127.0.0.1:8000/api/v1/)

---

## 🧪 Running Automated Tests

Run the full automated pytest suite (testing auth, template cloning, visual blocks, password protection, YES/NO responses, email alerts, and the complete creator-to-recipient journey):

```bash
cd backend
.\venv\Scripts\pytest
```

---

## 🐳 Docker Deployment

To launch the complete production stack (PostgreSQL 16, Redis, Django backend, and Nginx frontend) with one command:

```bash
docker-compose up --build
```
