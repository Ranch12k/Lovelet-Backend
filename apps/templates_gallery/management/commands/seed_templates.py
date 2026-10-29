from django.core.management.base import BaseCommand
from apps.templates_gallery.models import TemplateCategory, Template


class Command(BaseCommand):
    help = "Seed beautiful love letter and interactive greeting templates"

    def handle(self, *args, **options):
        self.stdout.write("Seeding romantic template categories and templates...")

        categories_data = [
            {"name": "Love Letters", "slug": "love-letters", "icon": "MailHeart", "description": "Classic and emotional romantic letters crafted for the one who holds your heart.", "sort_order": 1},
            {"name": "Proposals", "slug": "proposals", "icon": "Sparkles", "description": "Unforgettable digital proposals and 'Will you be mine?' questions.", "sort_order": 2},
            {"name": "Sorry & Apologies", "slug": "sorry-messages", "icon": "HeartHandshake", "description": "Sincere, gentle apologies and second chances expressed with tenderness.", "sort_order": 3},
            {"name": "YES/NO Questions", "slug": "yes-no-questions", "icon": "CheckCircle2", "description": "Playful, heart-racing interactive questions with customizable reactions.", "sort_order": 4},
            {"name": "Date Invitations", "slug": "date-invitations", "icon": "CalendarHeart", "description": "Charming invites for candlelit dinners, weekend getaways, or movie nights.", "sort_order": 5},
            {"name": "Birthday Wishes", "slug": "birthday", "icon": "Cake", "description": "Celebrate their special day with memories, love letters, and countdowns.", "sort_order": 6},
            {"name": "Anniversaries", "slug": "anniversary", "icon": "Hourglass", "description": "Celebrate your journey, milestones, and timeless commitment together.", "sort_order": 7},
            {"name": "Memories & Scrapbook", "slug": "memories", "icon": "Camera", "description": "A digital scrapbook capturing your favorite moments, polaroids, and inside jokes.", "sort_order": 8},
            {"name": "Cute & Funny", "slug": "cute-funny", "icon": "Smile", "description": "Lighthearted, adorable notes designed to make your favorite person smile.", "sort_order": 9},
            {"name": "Long Distance", "slug": "long-distance", "icon": "Compass", "description": "Bridge the miles between you with heartfelt notes and countdowns to reunion.", "sort_order": 10},
        ]

        category_objs = {}
        for cat in categories_data:
            obj, _ = TemplateCategory.objects.update_or_create(
                slug=cat['slug'],
                defaults=cat
            )
            category_objs[cat['slug']] = obj

        # Rich template definitions
        templates_data = [
            {
                "category_slug": "proposals",
                "title": "Will You Be My Valentine?",
                "slug": "will-you-be-my-valentine",
                "tagline": "The ultimate romantic question with animated envelope & sweet reaction",
                "description": "An enchanted experience opening with an animated rose-gold envelope, a poetic confession, photo scrapbook memories, and an interactive YES/NO proposal.",
                "thumbnail_url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "rose_gold",
                "envelope_seal_text": "BE MINE",
                "background_style": "romantic_gradient",
                "is_featured": True,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "The Envelope",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "My Beloved",
                                    "from_name": "Yours Always",
                                    "seal_text": "BE MINE",
                                    "teaser": "A special secret waiting for you inside... tap the seal to open ❤️",
                                    "theme": "rose_gold"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "My Dearest Thought",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "Every Day With You Is A Gift",
                                    "subtitle": "You walked into my life and suddenly everything made sense."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "From the quiet mornings to the late-night laughs, you have brought a warmth into my life that I never knew I was missing. I find myself smiling at random moments just remembering the way your eyes crinkle when you laugh.\n\nThank you for being my constant, my favorite listener, and the sweetest part of every single day.",
                                    "style": "serif",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "polaroid_gallery",
                                "sort_order": 3,
                                "config": {
                                    "items": [
                                        {"url": "https://images.unsplash.com/photo-1529333166437-7750a6dd5a70?w=500&auto=format&fit=crop&q=80", "caption": "The day we couldn't stop smiling"},
                                        {"url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?w=500&auto=format&fit=crop&q=80", "caption": "Under the quiet city stars"}
                                    ]
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 3,
                        "title": "The Big Question",
                        "transition_effect": "zoom",
                        "blocks": [
                            {
                                "block_type": "yes_no_question",
                                "sort_order": 1,
                                "config": {
                                    "prompt": "Will you be my Valentine? ❤️",
                                    "yes_label": "YES! A thousand times yes ❤️",
                                    "no_label": "Let me think... 🙈",
                                    "yes_message": "You just made me the happiest soul in the world! Happy Valentine's Day, my favorite person! ❤️✨",
                                    "no_message": "Take all the time you need, you still hold my whole heart. ❤️"
                                }
                            },
                            {
                                "block_type": "signature",
                                "sort_order": 2,
                                "config": {
                                    "sign_off": "With all my love,",
                                    "author": "Your Forever Person"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "category_slug": "sorry-messages",
                "title": "From The Bottom Of My Heart",
                "slug": "from-the-bottom-of-my-heart",
                "tagline": "A gentle, sincere apology to heal and reconnect",
                "description": "Express genuine regret and love with a peaceful aesthetic, soft lavender palette, and an open-hearted question to start again.",
                "thumbnail_url": "https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "midnight_velvet",
                "envelope_seal_text": "SORRY",
                "background_style": "lavender_mist",
                "is_featured": True,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "An Honest Letter",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "Someone I Truly Value",
                                    "from_name": "With A Heavy Heart",
                                    "seal_text": "SORRY",
                                    "teaser": "Please open this when you have a quiet moment... I wrote this for you.",
                                    "theme": "midnight_velvet"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "My Sincere Words",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "I'm Truly Sorry",
                                    "subtitle": "Your feelings mean the world to me, and I hurt you."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "I have been thinking non-stop about what happened, and I want to apologize without any excuses. I was wrong, and seeing you hurt because of me breaks my heart.\n\nOur bond is something I cherish more than words can express. I want to listen, learn, and make things right.",
                                    "style": "serif",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "yes_no_question",
                                "sort_order": 3,
                                "config": {
                                    "prompt": "Can we talk and give us another chance? 🕊️",
                                    "yes_label": "Yes, let's talk ❤️",
                                    "no_label": "I need some more time 🌿",
                                    "yes_message": "Thank you so much for your grace. I will never take you for granted. Let's talk whenever you're ready. ❤️",
                                    "no_message": "I completely respect your space and pace. I am here whenever you are ready."
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "category_slug": "date-invitations",
                "title": "A Special Date Just For Us",
                "slug": "a-special-date-just-for-us",
                "tagline": "Charming interactive invitation for a romantic night out",
                "description": "Invite them out in style with a candlelit theme, itinerary teaser, and interactive RSVP.",
                "thumbnail_url": "https://images.unsplash.com/photo-1517457373958-b7bdd4587205?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "vintage_parchment",
                "envelope_seal_text": "DATE NIGHT",
                "background_style": "sunset_glow",
                "is_featured": True,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "Your Invitation",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "The Cutest Person Alive",
                                    "from_name": "Your Secret Admirer",
                                    "seal_text": "DATE NIGHT",
                                    "teaser": "You are formally invited to an unforgettable evening... ✨",
                                    "theme": "vintage_parchment"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "The Plan",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "An Evening For Two",
                                    "subtitle": "Dress up nice, leave all your worries at home."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "✨ Delicious food at your favorite cozy spot\n🍸 Cocktails, laughter, and zero distractions\n🌙 Strolling under the night sky together\n\nAll I need is your company.",
                                    "style": "sans",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "yes_no_question",
                                "sort_order": 3,
                                "config": {
                                    "prompt": "Will you go on this date with me this weekend? 🥂",
                                    "yes_label": "Count me in! ❤️",
                                    "no_label": "Maybe next weekend? 🥺",
                                    "yes_message": "Woohoo! It's a date! Can't wait to see your smile. I'll pick you up! 🚗💫",
                                    "no_message": "Next weekend it is! Looking forward to it already!"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "category_slug": "birthday",
                "title": "Happy Birthday, My Star",
                "slug": "happy-birthday-my-star",
                "tagline": "Celebrate their birthday with sweet memories & warm wishes",
                "description": "A dazzling celebration card with festive confetti, photo scrapbook memories, and heartfelt wishes.",
                "thumbnail_url": "https://images.unsplash.com/photo-1513151233558-d860c5398176?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "blush_pink",
                "envelope_seal_text": "CELEBRATE",
                "background_style": "romantic_gradient",
                "is_featured": True,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "Birthday Delivery",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "Birthday Boy/Girl",
                                    "from_name": "With Huge Love",
                                    "seal_text": "CELEBRATE",
                                    "teaser": "Tap to unwrap your birthday surprise! 🎂🎉",
                                    "theme": "blush_pink"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "Wishes For You",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "Happy Birthday Beautiful!",
                                    "subtitle": "May your year ahead be as bright as your light."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "On this day, the world became a so much better place because you were born. Watching you grow, dream, and achieve your goals inspires me every single day.\n\nHere is to another year of inside jokes, endless adventures, and memories we will treasure forever!",
                                    "style": "serif",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "polaroid_gallery",
                                "sort_order": 3,
                                "config": {
                                    "items": [
                                        {"url": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=500&auto=format&fit=crop&q=80", "caption": "Birthday cheers and joy!"},
                                        {"url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=500&auto=format&fit=crop&q=80", "caption": "Making every moment count"}
                                    ]
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "category_slug": "anniversary",
                "title": "Our Beautiful Journey",
                "slug": "our-beautiful-journey",
                "tagline": "Celebrate years of love, growth, and companionship",
                "description": "An elegant scrapbook-style celebration of your time together, remembering how it all began.",
                "thumbnail_url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "rose_gold",
                "envelope_seal_text": "ALWAYS",
                "background_style": "romantic_gradient",
                "is_featured": True,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "Anniversary Card",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "My Love",
                                    "from_name": "Forever Yours",
                                    "seal_text": "ALWAYS",
                                    "teaser": "Happy Anniversary... a reflection on our story together ❤️",
                                    "theme": "rose_gold"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "Looking Back & Looking Ahead",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "Another Year Of Loving You",
                                    "subtitle": "And I would choose you all over again in every lifetime."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "Looking back on all the steps we have taken together, through challenges and victories, I am so proud of the life and love we have built.\n\nThank you for holding my hand through every chapter. Here is to all the unwritten pages waiting for us.",
                                    "style": "serif",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "signature",
                                "sort_order": 3,
                                "config": {
                                    "sign_off": "Yours through all the seasons,",
                                    "author": "Your Partner In Everything"
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "category_slug": "cute-funny",
                "title": "You Are My Favorite Human",
                "slug": "you-are-my-favorite-human",
                "tagline": "Playful, cute, and guaranteed to put a huge smile on their face",
                "description": "A cheerful, funny message loaded with sweet compliments and a playful questionnaire.",
                "thumbnail_url": "https://images.unsplash.com/photo-1507676184212-d03ab07a01bf?w=600&auto=format&fit=crop&q=80",
                "envelope_theme": "minimal_cream",
                "envelope_seal_text": "FOR YOU",
                "background_style": "clean_minimal",
                "is_featured": False,
                "is_free": True,
                "pages_data": [
                    {
                        "page_number": 1,
                        "title": "Cute Delivery",
                        "transition_effect": "fade",
                        "blocks": [
                            {
                                "block_type": "envelope",
                                "sort_order": 1,
                                "config": {
                                    "to_name": "Chief Goofball",
                                    "from_name": "Your #1 Fan",
                                    "seal_text": "FOR YOU",
                                    "teaser": "Special delivery for the coolest person in town! 💌",
                                    "theme": "minimal_cream"
                                }
                            }
                        ]
                    },
                    {
                        "page_number": 2,
                        "title": "Scientific Proof",
                        "transition_effect": "slide",
                        "blocks": [
                            {
                                "block_type": "heading",
                                "sort_order": 1,
                                "config": {
                                    "title": "Certified 100% Best Human",
                                    "subtitle": "According to extensive research conducted by me."
                                }
                            },
                            {
                                "block_type": "text",
                                "sort_order": 2,
                                "config": {
                                    "content": "I like you more than:\n🍕 Extra cheese pizza\n☕ Sunday morning sleep-ins\n📱 100% phone battery with free high-speed wifi\n\nThat is saying A LOT.",
                                    "style": "sans",
                                    "align": "center"
                                }
                            },
                            {
                                "block_type": "yes_no_question",
                                "sort_order": 3,
                                "config": {
                                    "prompt": "Do you love me at least 1% as much? 🥺",
                                    "yes_label": "Way more than that! ❤️",
                                    "no_label": "Maybe 0.5% 😉",
                                    "yes_message": "Yesss! I knew it! Sending you 1,000 virtual hugs right now! 🤗❤️",
                                    "no_message": "Hey! I will take that 0.5% and turn it into 100% soon! 😄"
                                }
                            }
                        ]
                    }
                ]
            }
        ]

        created_count = 0
        for tpl in templates_data:
            cat_slug = tpl.pop("category_slug")
            category = category_objs[cat_slug]
            _, created = Template.objects.update_or_create(
                slug=tpl["slug"],
                defaults={**tpl, "category": category}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(categories_data)} categories and {len(templates_data)} templates!"))
