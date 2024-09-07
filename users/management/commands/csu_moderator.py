from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='moderator@localhost',
            first_name='admin',
            is_superuser=False,
            is_staff=True,
            is_active=True,
        )
        user.set_password('123')
        user.save()