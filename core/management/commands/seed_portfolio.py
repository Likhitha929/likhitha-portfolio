"""
Seed the portfolio with Likhitha Goru's CV content.

    python manage.py seed_portfolio          # add/update rows
    python manage.py seed_portfolio --flush  # wipe portfolio tables first
"""
from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from blog.models import Category, Post
from core.models import (
    Achievement,
    CodingProfile,
    Education,
    Experience,
    ExperienceBullet,
    Language,
    Profile,
    Project,
    Skill,
    SkillCategory,
)


class Command(BaseCommand):
    help = "Populate the database with portfolio content from the CV."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete existing portfolio rows before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            for model in (
                ExperienceBullet, Experience, Skill, SkillCategory, Education,
                Project, Achievement, CodingProfile, Language, Profile, Post, Category,
            ):
                model.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing portfolio data removed."))

        self._profile()
        self._skills()
        self._education()
        self._experience()
        self._projects()
        self._achievements()
        self._coding_profiles()
        self._languages()
        self._blog()

        self.stdout.write(self.style.SUCCESS("Portfolio seeded successfully."))

    # ------------------------------------------------------------------ profile
    def _profile(self):
        Profile.objects.update_or_create(
            full_name="Likhitha Goru",
            defaults={
                "tagline": "Developer ~ Engineer",
                "typed_roles": "machine learning models, NLP & RAG pipelines, "
                "full-stack Django apps, data-driven products",
                "about": (
                    "I'm an M.Tech student in Information Technology at NIT Raipur, "
                    "building machine learning systems and the web applications that "
                    "make them usable. My work sits between the two: training a "
                    "Transformer from scratch one week, wiring up Google OAuth and a "
                    "document pipeline the next.\n\n"
                    "I care about systems that hold up in practice. That means "
                    "measuring what a model actually does rather than what I hoped it "
                    "would, and designing schemas flexible enough that adding a new "
                    "document type doesn't mean rewriting the backend.\n\n"
                    "I write Python, C++ and C, work with PyTorch and TensorFlow, and "
                    "build with Django and Flask. I qualified GATE 2025 and served as "
                    "General Secretary of my college's lecture series club, where I "
                    "learned that explaining an idea well is its own engineering problem."
                ),
                "email": "likhithagoru929@gmail.com",
                "phone": "+91 7569373825",
                "location": "Raipur, Chhattisgarh, India",
                "github_username": "",
                "show_github_stats": False,
                "linkedin_url": "https://www.linkedin.com/in/likhithagoru",
                "available_for_work": True,
                "is_active": True,
            },
        )
        self.stdout.write("  · profile")

    # ------------------------------------------------------------------- skills
    def _skills(self):
        data = [
            ("Programming Languages", "bi-code-slash", "Languages I work in daily.", 1, [
                ("Python", 95, True), ("C++", 85, True), ("C", 80, True), ("SQL", 80, False),
            ]),
            ("Machine Learning", "bi-cpu", "Classical ML, end to end.", 2, [
                ("Supervised Learning", 90, True), ("Unsupervised Learning", 85, True),
                ("Feature Engineering", 0, False), ("Model Evaluation", 0, False),
                ("Scikit-learn", 0, False), ("XGBoost", 0, False), ("LightGBM", 0, False),
            ]),
            ("Deep Learning", "bi-diagram-3", "Neural architectures and optimisation.", 3, [
                ("Neural Networks (ANN, CNN, RNN)", 88, True), ("LSTM / GRU", 0, False),
                ("Model Optimization", 0, False), ("TensorFlow", 0, False),
                ("PyTorch", 0, False),
            ]),
            ("LLMs & NLP", "bi-chat-square-text", "Language models and retrieval.", 4, [
                ("Transformers", 90, True), ("RAG", 88, True),
                ("Prompt Engineering", 0, False), ("Hugging Face", 0, False),
                ("Tokenization", 0, False), ("Embeddings", 0, False),
                ("N-gram Models", 0, False), ("HMM", 0, False),
            ]),
            ("Data Science & Analysis", "bi-bar-chart-line", "Finding the signal.", 5, [
                ("Exploratory Data Analysis", 88, True), ("Data Cleaning", 0, False),
                ("Data Visualization", 0, False), ("Pandas", 0, False), ("NumPy", 0, False),
            ]),
            ("Web Development", "bi-window-stack", "Python-backed full stack.", 6, [
                ("Django", 90, True), ("HTML / CSS", 88, True),
                ("Django REST Framework", 0, False), ("Flask", 0, False),
                ("Streamlit", 0, False), ("Google APIs / OAuth2", 0, False),
            ]),
            ("Core CS & Tools", "bi-hdd-stack", "The fundamentals.", 7, [
                ("Data Structures & Algorithms", 90, True), ("OOP", 0, False),
                ("DBMS", 0, False), ("Operating Systems", 0, False),
                ("Computer Networks", 0, False), ("Git / GitHub", 0, False),
            ]),
        ]

        for name, icon, description, order, skills in data:
            category, _ = SkillCategory.objects.update_or_create(
                name=name,
                defaults={"icon": icon, "description": description, "order": order},
            )
            for index, (skill_name, proficiency, featured) in enumerate(skills):
                Skill.objects.update_or_create(
                    category=category,
                    name=skill_name,
                    defaults={
                        "proficiency": proficiency or 80,
                        "is_featured": featured,
                        "order": index,
                    },
                )
        self.stdout.write("  · skills")

    # ---------------------------------------------------------------- education
    def _education(self):
        entries = [
            ("National Institute of Technology, Raipur", "M.Tech",
             "Information Technology", "Raipur, Chhattisgarh", 2025, None,
             "Aggregate: 90.2%", 1),
            ("Rajiv Gandhi University of Knowledge Technologies", "B.Tech",
             "Computer Science and Engineering", "Srikakulam, AP", 2021, 2025,
             "Aggregate: 90%", 2),
            ("Rajiv Gandhi University of Knowledge Technologies", "Intermediate",
             "Maths, Physics and Chemistry", "Srikakulam, AP", 2019, 2021,
             "Aggregate: 97.8%", 3),
            ("A.P Model School", "SSC", "", "Andhra Pradesh", 2018, 2019,
             "Aggregate: 100%", 4),
        ]
        for inst, degree, field, loc, start, end, score, order in entries:
            Education.objects.update_or_create(
                institution=inst,
                degree=degree,
                defaults={
                    "field_of_study": field,
                    "location": loc,
                    "start_year": start,
                    "end_year": end,
                    "score": score,
                    "order": order,
                },
            )
        self.stdout.write("  · education")

    # --------------------------------------------------------------- experience
    def _experience(self):
        experience, _ = Experience.objects.update_or_create(
            role="Data Science Intern",
            organisation="Andhra Pradesh State Skill Development Corporation (APSSDC)",
            defaults={
                "location": "Andhra Pradesh, India",
                "start_date": date(2024, 5, 1),
                "end_date": date(2024, 6, 30),
                "summary": "Built an end-to-end sentiment analysis pipeline over real "
                           "customer feedback data.",
                "tech_stack": "Python, Machine Learning, NLP, Scikit-learn, Pandas, NLTK",
                "order": 1,
            },
        )
        bullets = [
            "Developed an NLP-based sentiment analysis model achieving 88% accuracy.",
            "Processed and analyzed 5,000+ records using data cleaning, preprocessing "
            "and feature engineering.",
            "Improved data quality by 30% through effective preprocessing and validation.",
            "Optimized the inference pipeline, reducing prediction time by 20%.",
        ]
        experience.bullets.all().delete()
        for index, text in enumerate(bullets):
            ExperienceBullet.objects.create(experience=experience, text=text, order=index)
        self.stdout.write("  · experience")

    # ----------------------------------------------------------------- projects
    def _projects(self):
        projects = [
            {
                "title": "Doc Generator App",
                "subtitle": "Schema-driven document generation on the Google Workspace APIs",
                "category": "web",
                "badge": "Full Stack",
                "short_description": "A full-stack platform that generates documents from "
                                     "reusable Google Docs templates, using dynamic JSON "
                                     "field schemas so new document types need no code changes.",
                "description": (
                    "Most document generators hardcode one template per document type. This "
                    "one treats the schema as data: a JSON field definition describes the "
                    "placeholders, so adding a new document type is a configuration change "
                    "rather than a deployment.\n"
                    "Google OAuth2 handles authentication, the Docs API's batchUpdate "
                    "performs placeholder replacement in a single call, and the Drive API "
                    "manages access and export."
                ),
                "highlights": "Schema-driven design supporting unlimited document types\n"
                              "Google OAuth2 authentication end to end\n"
                              "Docs API batchUpdate for atomic placeholder replacement\n"
                              "Drive API integration for document access and export",
                "tech_stack": "Django, Django REST Framework, Google Docs API, "
                              "Google Drive API, OAuth2, Python",
                "is_featured": True,
                "order": 1,
            },
            {
                "title": "Retrieval-Augmented Narrative Consistency Verification",
                "subtitle": "A 10.7M-parameter Transformer trained from scratch",
                "category": "nlp",
                "badge": "Research",
                "short_description": "A BERT-style Transformer paired with a hybrid BM25 "
                                     "and semantic retrieval RAG pipeline, verifying whether "
                                     "narrative statements stay consistent with their source text.",
                "description": (
                    "The encoder was designed and trained from scratch at 10.7M parameters "
                    "rather than fine-tuned from a checkpoint, so every architectural choice "
                    "could be measured independently.\n"
                    "Retrieval combines lexical BM25 with dense semantic search — each finds "
                    "evidence the other misses, and the combination moved accuracy more than "
                    "any single modelling change."
                ),
                "highlights": "97.56% accuracy on the verification task\n"
                              "0.97 Macro F1 and 0.99 ROC-AUC\n"
                              "Hybrid BM25 + dense retrieval for evidence selection\n"
                              "10.7M-parameter encoder trained from scratch",
                "tech_stack": "PyTorch, Transformers, RAG, BM25, NLP, Python",
                "is_featured": True,
                "order": 2,
            },
            {
                "title": "AI-Powered Multimodal E-commerce Price Prediction System",
                "subtitle": "Product text and images feeding a stacked ensemble",
                "category": "ml",
                "badge": "End-to-end",
                "short_description": "An end-to-end system predicting product prices from "
                                     "both descriptions and images, served through a Streamlit "
                                     "app for real-time predictions and automated reporting.",
                "description": (
                    "Textual features cover keywords, quality indicators and numeric analysis "
                    "of the listing copy; deep image features come from pre-trained MobileNetV2 "
                    "and ResNet50 backbones.\n"
                    "Predictions come from a super ensemble of XGBoost, LightGBM, Random "
                    "Forest, Gradient Boosting and Ridge Regression, wrapped in a Streamlit "
                    "interface with automated reporting."
                ),
                "highlights": "Multimodal features from product text and images\n"
                              "MobileNetV2 and ResNet50 as frozen feature extractors\n"
                              "Five-model stacked ensemble for the final prediction\n"
                              "Streamlit app for real-time pricing and reports",
                "tech_stack": "Python, TensorFlow, Scikit-learn, XGBoost, LightGBM, "
                              "Streamlit, NLP",
                "is_featured": True,
                "order": 3,
            },
        ]

        for data in projects:
            Project.objects.update_or_create(title=data["title"], defaults=data)
        self.stdout.write("  · projects")

    # ------------------------------------------------------------- achievements
    def _achievements(self):
        awards = [
            {
                "title": "Qualified GATE 2025",
                "issuer": "All India",
                "period": "2025",
                "icon": "bi-patch-check",
                "description": "Qualified the Graduate Aptitude Test in Engineering 2025, "
                               "demonstrating strong proficiency in core technical subjects.",
                "order": 1,
            },
            {
                "title": "General Secretary, SGC Lecture Series Club",
                "issuer": "RGUKT Srikakulam",
                "period": "2022 – 2024",
                "icon": "bi-people",
                "description": "Led event organization and academic discussions for the club.\n"
                               "Coordinated guest lectures, workshops and knowledge-sharing "
                               "sessions to widen learning opportunities on campus.",
                "order": 2,
            },
            {
                "title": "Event Organizer, College Tech Fest",
                "issuer": "RGUKT Srikakulam",
                "period": "2023 – 2024",
                "icon": "bi-calendar-event",
                "description": "Managed logistics and scheduling for technical events.\n"
                               "Collaborated with faculty and students on sessions and "
                               "project showcases.",
                "order": 3,
            },
        ]
        certifications = [
            {
                "title": "Internship Completion Certificate",
                "issuer": "S2 Tech",
                "period": "2022 – 2023",
                "icon": "bi-award",
                "order": 1,
            },
        ]

        for data in awards:
            Achievement.objects.update_or_create(
                title=data["title"], kind="award", defaults={**data, "kind": "award"}
            )
        for data in certifications:
            Achievement.objects.update_or_create(
                title=data["title"], kind="cert", defaults={**data, "kind": "cert"}
            )
        self.stdout.write("  · achievements")

    # ----------------------------------------------------------- coding profiles
    def _coding_profiles(self):
        entries = [
            ("LeetCode", "Likhitha_Goru_lc",
             "https://leetcode.com/u/Likhitha_Goru_lc/", "bi-code-square", 1),
            ("GeeksforGeeks", "Likhitha_Goru_gfg",
             "https://www.geeksforgeeks.org/user/Likhitha_Goru_gfg/", "bi-braces", 2),
        ]
        for platform, username, url, icon, order in entries:
            CodingProfile.objects.update_or_create(
                platform=platform,
                defaults={"username": username, "url": url, "icon": icon, "order": order},
            )
        self.stdout.write("  · coding profiles")

    # ---------------------------------------------------------------- languages
    def _languages(self):
        for order, (name, level) in enumerate([("English", "Fluent"), ("Telugu", "Fluent")], 1):
            Language.objects.update_or_create(name=name, defaults={"level": level, "order": order})
        self.stdout.write("  · languages")

    # --------------------------------------------------------------------- blog
    def _blog(self):
        ml_category, _ = Category.objects.get_or_create(name="Machine Learning")
        web_category, _ = Category.objects.get_or_create(name="Web Development")

        posts = [
            {
                "title": "Why schema-driven beats one-template-per-document",
                "category": web_category,
                "tags": "django, google-api, architecture, oauth2",
                "excerpt": "The first version of my document generator needed a code change "
                           "for every new document type. The second one didn't.",
                "body": (
                    "The obvious way to build a document generator is one template, one "
                    "handler, one endpoint. It works beautifully until someone asks for a "
                    "fourth document type and you realise you've written the same function "
                    "three times.\n\n"
                    "The version I ended up with treats the schema as data. A JSON field "
                    "definition describes what placeholders a template has and what each "
                    "one expects. Adding a document type means adding a row, not writing "
                    "and deploying a handler.\n\n"
                    "The Google Docs API rewards this design. Its batchUpdate endpoint "
                    "takes a list of replacement operations and applies them in one call, "
                    "so a schema with twenty placeholders costs exactly as much as one with "
                    "two. Combined with OAuth2 for access and the Drive API for export, the "
                    "whole pipeline stays under a few hundred lines."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(days=6),
            },
            {
                "title": "BM25 and embeddings find different things",
                "category": ml_category,
                "tags": "RAG, retrieval, NLP, transformers",
                "excerpt": "I assumed dense retrieval would make keyword search redundant. "
                           "Measuring it changed my mind.",
                "body": (
                    "When I started the narrative consistency project I expected semantic "
                    "search to dominate. Embeddings understand meaning; keyword matching is "
                    "the thing embeddings were invented to replace.\n\n"
                    "That isn't what the retrieval logs showed. BM25 reliably caught exact "
                    "names, numbers and rare terms that embeddings smoothed into their "
                    "neighbours. Dense search caught paraphrases that shared no vocabulary "
                    "with the query at all. Each method's failures were the other's "
                    "successes.\n\n"
                    "Combining them was worth more than any change I made to the model "
                    "itself. The final system reached 97.56% accuracy with a 0.99 ROC-AUC, "
                    "and most of the distance from the baseline came from what the retriever "
                    "put in front of the encoder rather than the encoder's own capacity."
                ),
                "status": Post.Status.PUBLISHED,
                "published_at": timezone.now() - timezone.timedelta(days=21),
            },
        ]

        for data in posts:
            Post.objects.update_or_create(title=data["title"], defaults=data)
        self.stdout.write("  · blog posts")
