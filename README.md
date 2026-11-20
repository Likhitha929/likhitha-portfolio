# Likhitha Goru — Developer Portfolio

A database-driven personal portfolio built with **Django 5**, **Bootstrap 5**, custom CSS and vanilla JavaScript. Every section — projects, skills, experience, education, achievements, blog posts, contact messages — is a Django model editable from the admin, so updating the site never means editing HTML.

---

## Features

- **Single-page home** with numbered sections, an animated typing role, scroll-reveal, count-up stats and scroll-spy navigation
- **Full Django admin CMS** — inlines, custom actions, `list_editable` fields, prepopulated slugs
- **Projects** — list page with category filtering and search, plus a detail page per project
- **Blog app** — categories, tags, drafts vs published (custom `PublishedManager`), pagination, view counter, auto reading-time
- **Contact form** — server-side validation, honeypot spam trap, messages saved to the DB and readable in the admin, optional SMTP notification
- **CV download** served from static files
- **Production-ready** — WhiteNoise static serving, env-based settings, security headers when `DEBUG=False`, custom 404/500 pages
- Fully responsive, keyboard accessible, respects `prefers-reduced-motion`

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 5.2, Python 3.12 |
| Frontend | HTML5, CSS3, JavaScript (no build step), Bootstrap 5.3 |
| Database | SQLite (dev) — swap `DATABASES` for PostgreSQL in production |
| Static files | WhiteNoise (Bootstrap vendored locally, works offline) |
| Server | Gunicorn |

---

## Quick start

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env              # Windows: copy .env.example .env

# 4. Set up the database and load the CV content
python manage.py migrate
python manage.py seed_portfolio

# 5. Create your admin login
python manage.py createsuperuser

# 6. Run it
python manage.py runserver
```

- Site: <http://127.0.0.1:8000/>
- Admin: <http://127.0.0.1:8000/admin/>

---

## Editing your content

Everything lives in the admin at `/admin/`:

| What to change | Where |
|---|---|
| Name, tagline, bio, photo, social links | **Core → Profiles** |
| Skill groups and individual skills | **Core → Skill categories** (skills are inline) |
| Degrees and scores | **Core → Education** |
| Jobs and internships | **Core → Experiences** (bullets are inline) |
| Portfolio projects | **Core → Projects** |
| Awards and certifications | **Core → Achievements** |
| LeetCode / GeeksforGeeks | **Core → Coding profiles** |
| Blog articles | **Blog → Posts** |
| Messages people send you | **Core → Contact messages** |

Two conventions worth knowing:

- A skill marked **featured** renders as an animated meter; the rest render as tags.
- In **Project → highlights** and **Achievement → description**, one line becomes one bullet point.

### Adding a photo

Open **Core → Profiles → Likhitha Goru** and upload an image to *Photo*. Without one, the hero shows your initials in a coloured squircle.

For deployment, a better option is to put the image at `static/img/profile.jpg` and reference it there — uploaded files in `media/` do not survive restarts on free hosting.

### Turning on the GitHub stat cards

They are **off by default**, because empty stats look worse than no stats. Once your GitHub has public repositories, open **Core → Profiles**, fill in *Github username* and tick *Show github stats*.

---

## Deployment (Render, free)

1. Push this repo to GitHub.
2. On [render.com](https://render.com): **New +** → **Web Service** → connect the repo.
3. Settings:
   - **Language:** Python 3 — *not Docker, even though a Dockerfile exists*
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn config.wsgi:application`
   - **Instance Type:** Free
4. Environment variables:

| Key | Value |
|---|---|
| `SECRET_KEY` | click Generate |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.onrender.com` |
| `DJANGO_SUPERUSER_USERNAME` | your admin username |
| `DJANGO_SUPERUSER_EMAIL` | your email |
| `DJANGO_SUPERUSER_PASSWORD` | a strong password |

`build.sh` runs migrations, seeds the content and creates the admin user on every deploy.

**Two things to know about the free tier:**

- The service sleeps after 15 minutes idle and takes about a minute to wake.
- There is no persistent disk, so the database resets on restart. Content is rebuilt from `seed_portfolio` each deploy, which means edits made through the *live* admin are lost. To make content changes permanent, edit locally and either update `seed_portfolio.py` or export a fixture:

```bash
mkdir -p fixtures
python manage.py dumpdata core blog --indent 2 --exclude core.contactmessage > fixtures/content.json
# then change build.sh to: python manage.py loaddata fixtures/content.json
```

---

## Contact form email

Without SMTP credentials, messages are still **saved to the database** and visible in the admin — the email is just printed to the console. For real email, fill the `EMAIL_*` values in `.env`. Gmail requires an [App Password](https://myaccount.google.com/apppasswords), not your account password.

---

## Useful commands

```bash
python manage.py seed_portfolio            # add or update seeded content
python manage.py seed_portfolio --flush    # wipe portfolio tables, then reseed
python manage.py collectstatic             # gather static files for production
python manage.py check --deploy            # production readiness audit
```
