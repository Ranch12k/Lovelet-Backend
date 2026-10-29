from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Initialize default administrator account"

    def handle(self, *args, **options):
        email = "admin@lovelink.app"
        username = "admin@lovelink.app"
        password = "AdminLove2026!"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': 'Admin',
                'is_staff': True,
                'is_superuser': True
            }
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created default admin account: {email} / {password}"))
        else:
            self.stdout.write(self.style.WARNING("Admin account already exists."))
