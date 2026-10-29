# LoveLink — System Architecture & Specification Blueprint

## 1. System Architecture

```
+----------------------------------------------------------------------------------------------------+
|                                         CLIENT LAYER                                               |
|                                                                                                    |
|   +------------------------------------+          +--------------------------------------------+   |
|   |   Creator Studio (React + Vite)    |          |    Recipient Experience (/l/:slug)         |   |
|   |   - Visual Multi-Page Block Editor |          |    - Animated Wax Seal & Envelope Gift     |   |
|   |   - Live Responsive Split Preview  |          |    - Floating Particles & Confetti Canvas  |   |
|   |   - Template Marketplace / Gallery |          |    - Typewriter, Scrapbook, Polaroid       |   |
|   |   - Responses & Analytics Stream   |          |    - Interactive YES/NO Decision Engine    |   |
|   |   - Media Manager & Asset Crop     |          |    - Password Gate with Rate-Limiting      |   |
|   +-----------------+------------------+          +--------------------+-----------------------+   |
+---------------------|--------------------------------------------------|---------------------------+
                      | HTTPS / REST JSON API                            | Anonymous / Token Auth
                      v                                                  v
+----------------------------------------------------------------------------------------------------+
|                                    BACKEND APPLICATION LAYER (Django REST)                        |
|                                                                                                    |
|   +-----------------------+  +----------------------+  +---------------------+  +--------------+   |
|   | accounts & auth       |  | experiences & pages  |  | interactions        |  | media_assets |   |
|   | - Token/Session Auth  |  | - Draft autosave     |  | - YES/NO dispatcher |  | - Safe MIME  |   |
|   | - Verification & PW   |  | - Slug resolver      |  | - Anti-spam check   |  | - Compression|   |
|   | - RBAC (Admin/Creator)|  | - Password hashing   |  | - Duplicate guards  |  | - Private ACL|   |
|   +-----------------------+  +----------------------+  +---------------------+  +--------------+   |
|   +-----------------------+  +----------------------+  +---------------------+  +--------------+   |
|   | templates_gallery     |  | notifications        |  | moderation          |  | analytics    |   |
|   | - Preset Categories   |  | - Transactional mail |  | - Abuse reporting   |  | - Privacy OK |   |
|   | - Clone & Customize   |  | - Creator alerts     |  | - Admin controls    |  | - Visit ctrs |   |
|   +-----------------------+  +----------------------+  +---------------------+  +--------------+   |
+----------------------------------------------------------------------------------------------------+
                      |                                                  |
                      v                                                  v
+------------------------------------------+       +-------------------------------------------------+
|          PERSISTENCE LAYER               |       |         ASYNC & NOTIFICATION WORKERS            |
|                                          |       |                                                 |
|  - PostgreSQL / SQLite Engine            |       |  - Celery Worker / In-Process Async Task Queue  |
|  - Normalized Relational Schema          |       |  - Redis Cache & Rate-Limiting Broker           |
|  - JSONB for dynamic Block Attributes    |       |  - SMTP Transactional Email Dispatcher          |
+------------------------------------------+       +-------------------------------------------------+
```

---

## 2. Directory & Folder Structure

```
c:/lOVE/
|-- backend/
|   |-- manage.py
|   |-- requirements.txt
|   |-- lovelink/
|   |   |-- __init__.py
|   |   |-- settings.py
|   |   |-- urls.py
|   |   |-- wsgi.py
|   |   |-- celery.py
|   |-- apps/
|   |   |-- accounts/
|   |   |   |-- models.py (User, Profile, PasswordResetToken)
|   |   |   |-- views.py, serializers.py, urls.py, permissions.py
|   |   |-- templates_gallery/
|   |   |   |-- models.py (TemplateCategory, Template)
|   |   |   |-- views.py, serializers.py, urls.py, fixtures/seed_data.py
|   |   |-- experiences/
|   |   |   |-- models.py (Experience, ExperiencePage, ContentBlock, ExperienceAccessSettings, Analytics)
|   |   |   |-- views.py, serializers.py, urls.py, services.py
|   |   |-- interactions/
|   |   |   |-- models.py (Question, QuestionOption, Response)
|   |   |   |-- views.py, serializers.py, urls.py
|   |   |-- notifications/
|   |   |   |-- models.py (EmailNotification, NotificationPreference)
|   |   |   |-- tasks.py, services.py, views.py, urls.py
|   |   |-- media_assets/
|   |   |   |-- models.py (MediaAsset)
|   |   |   |-- views.py, serializers.py, urls.py, utils.py
|   |   |-- moderation/
|   |       |-- models.py (AbuseReport)
|   |       |-- views.py, serializers.py, urls.py
|   |-- media/ (Uploaded photos, optimized thumbnails)
|   |-- static/
|-- frontend/
|   |-- index.html
|   |-- package.json
|   |-- vite.config.js
|   |-- tailwind.config.js
|   |-- postcss.config.js
|   |-- src/
|       |-- main.jsx
|       |-- App.jsx
|       |-- index.css (Custom design system tokens, typography, romantic animations)
|       |-- api/
|       |   |-- client.js (Axios instance with auto-token auth & interceptors)
|       |   |-- auth.js, experiences.js, templates.js, responses.js, media.js
|       |-- components/
|       |   |-- common/ (Button, Input, Modal, Badge, Dropdown, Loader, Toast)
|       |   |-- layout/ (Navbar, Sidebar, DashboardLayout, Footer)
|       |   |-- editor/
|       |   |   |-- Canvas.jsx, BlockPalette.jsx, BlockPropertyPanel.jsx
|       |   |   |-- PageNavigator.jsx, EnvelopeSettingsModal.jsx, ShareModal.jsx
|       |   |-- blocks/ (Renderers for Envelope, Heading, LoveLetterText, PolaroidScrapbook,
|       |   |            YesNoQuestion, PhotoCarousel, FloatingHearts, MusicPlayer, Countdown)
|       |   |-- recipient/ (GiftUnboxWrapper, PasswordGate, PageTransition, CelebrationConfetti)
|       |-- context/
|       |   |-- AuthContext.jsx
|       |   |-- EditorContext.jsx
|       |   |-- ToastContext.jsx
|       |-- pages/
|       |   |-- LandingPage.jsx
|       |   |-- Auth/ (LoginPage, RegisterPage, ForgotPasswordPage)
|       |   |-- Dashboard/ (OverviewPage, MyExperiencesPage, ResponsesPage, MediaPage, SettingsPage)
|       |   |-- EditorPage.jsx (Full-screen interactive studio)
|       |   |-- TemplateGalleryPage.jsx
|       |   |-- RecipientExperiencePage.jsx (Public `/l/:slug` viewer)
|       |   |-- AdminPortalPage.jsx
|-- docker-compose.yml
|-- Dockerfile.backend
|-- Dockerfile.frontend
|-- .env.example
|-- README.md
```

---

## 3. Database Entity Relationship Model

```
+------------------+         +---------------------+         +----------------------+
|      User        | 1 --- 1 |       Profile       | 1 --- * | NotificationPreference|
+------------------+         +---------------------+         +----------------------+
| id (PK)          |         | user_id (FK)        |         | user_id (FK)         |
| email (Unique)   |         | display_name        |         | email_on_response    |
| password_hash    |         | avatar_url          |         | weekly_digest        |
| is_verified      |         | storage_used_bytes  |         +----------------------+
| is_staff / admin |         | plan_tier           |
+--------+---------+         +---------------------+
         | 1
         |
         +----------------------------------+
         |                                  |
         v *                                v *
+------------------+               +-------------------+
|    Experience    |               |    MediaAsset     |
+------------------+               +-------------------+
| id (UUID, PK)    |               | id (UUID, PK)     |
| user_id (FK)     |               | user_id (FK)      |
| slug (Unique)    |               | file (ImageField) |
| title            |               | original_name     |
| status           |               | mime_type         |
| envelope_theme   |               | file_size_bytes   |
| music_url        |               | width, height     |
| background_style |               +-------------------+
| expires_at       |
| view_count       |
+--------+---------+
         | 1
         |--------------------------------------+------------------------------------+
         v 1                                    v *                                  v *
+-------------------------+            +-------------------+               +-------------------+
| ExperienceAccessSettings|            |  ExperiencePage   |               |    Analytics      |
+-------------------------+            +-------------------+               +-------------------+
| experience_id (FK, 1:1) |            | id (UUID, PK)     |               | id (PK)           |
| is_password_protected   |            | experience_id(FK) |               | experience_id(FK) |
| password_hash (Argon2)  |            | page_number (int) |               | ip_hash (privacy) |
| allow_change_answer     |            | title             |               | user_agent        |
| notify_on_response      |            | transition_effect |               | timestamp         |
+-------------------------+            +---------+---------+               +-------------------+
                                                 | 1
                                                 v *
                                       +-------------------+
                                       |   ContentBlock    |
                                       +-------------------+
                                       | id (UUID, PK)     |
                                       | page_id (FK)      |
                                       | block_type (Enum) |
                                       | sort_order (int)  |
                                       | config (JSONB)    |
                                       +---------+---------+
                                                 | 1 (if question block)
                                                 v 0..1
                                       +-------------------+
                                       |     Question      |
                                       +-------------------+
                                       | id (UUID, PK)     |
                                       | block_id (FK)     |
                                       | prompt_text       |
                                       | question_type     |
                                       +---------+---------+
                                                 | 1
                                                 v *
                                       +-------------------+
                                       |     Response      |
                                       +-------------------+
                                       | id (UUID, PK)     |
                                       | question_id (FK)  |
                                       | experience_id(FK) |
                                       | respondent_token  |
                                       | answer_text       |
                                       | submitted_at      |
                                       +---------+---------+
                                                 | 1
                                                 v 0..1
                                       +--------------------+
                                       | EmailNotification  |
                                       +--------------------+
                                       | id (UUID, PK)      |
                                       | response_id (FK)   |
                                       | recipient_email    |
                                       | status (sent/fail) |
                                       | sent_at            |
                                       +--------------------+
```

---

## 4. REST API Endpoint Specification

### Authentication & Accounts
- `POST /api/v1/auth/register/` - Register new creator
- `POST /api/v1/auth/login/` - Login and obtain Auth Token
- `POST /api/v1/auth/logout/` - Invalidate session/token
- `GET  /api/v1/auth/me/` - Retrieve current creator profile & storage usage
- `PUT  /api/v1/auth/me/` - Update profile & preferences
- `POST /api/v1/auth/change-password/` - Secure password rotation

### Templates Marketplace
- `GET  /api/v1/templates/` - Filterable catalog (by category, featured, tags)
- `GET  /api/v1/templates/categories/` - List categories
- `GET  /api/v1/templates/:slug/` - Full template preview schema
- `POST /api/v1/templates/:slug/clone/` - Clone template into user's private workspace

### Experiences (Creator Workspace)
- `GET    /api/v1/experiences/` - List user's draft & published experiences
- `POST   /api/v1/experiences/` - Create new experience from scratch or template
- `GET    /api/v1/experiences/:id/` - Complete experience bundle with pages and blocks
- `PUT    /api/v1/experiences/:id/` - Update experience metadata, theme, music, settings
- `DELETE /api/v1/experiences/:id/` - Remove experience
- `POST   /api/v1/experiences/:id/duplicate/` - Duplicate experience
- `POST   /api/v1/experiences/:id/publish/` - Toggle published status & generate slug
- `POST   /api/v1/experiences/:id/regenerate-slug/` - Issue new secret URL

### Pages & Blocks (Visual Editor)
- `POST   /api/v1/experiences/:id/pages/` - Add new page
- `PUT    /api/v1/experiences/:id/pages/:page_id/` - Update page layout/transition
- `DELETE /api/v1/experiences/:id/pages/:page_id/` - Delete page
- `POST   /api/v1/experiences/:id/pages/:page_id/blocks/` - Add block
- `PUT    /api/v1/experiences/:id/pages/:page_id/blocks/reorder/` - Reorder blocks
- `PUT    /api/v1/experiences/:id/pages/:page_id/blocks/:block_id/` - Update block config
- `DELETE /api/v1/experiences/:id/pages/:page_id/blocks/:block_id/` - Delete block

### Public Recipient Experience (Unauthenticated with Gatekeeper)
- `GET  /api/v1/public/experience/:slug/` - Fetch safe public package (Metadata, password requirement)
- `POST /api/v1/public/experience/:slug/unlock/` - Verify experience password, return temp view session
- `POST /api/v1/public/experience/:slug/respond/` - Submit answer to YES/NO question
- `POST /api/v1/public/experience/:slug/visit/` - Log privacy-conscious view analytics

### Media Management
- `GET    /api/v1/media/` - List uploaded photos/assets with storage quota
- `POST   /api/v1/media/upload/` - Upload with MIME check, resize & thumbnailing
- `DELETE /api/v1/media/:id/` - Delete media asset

### Responses & Notifications
- `GET /api/v1/responses/` - List responses across user's experiences
- `GET /api/v1/experiences/:id/responses/` - Detailed response log for specific experience
- `GET /api/v1/dashboard/stats/` - Aggregate metrics (Total views, response rate, active links)

### Admin & Moderation
- `GET  /api/v1/admin/stats/` - Platform health & volume stats
- `GET  /api/v1/admin/reports/` - Review abuse reports
- `POST /api/v1/admin/experiences/:id/take-down/` - Moderate toxic/violating experiences
