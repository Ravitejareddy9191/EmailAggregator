from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from orders.models import UserProfile
import sys
import os

# Add email parser path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../email_to_db'))

try:
    from run_email_parser import parse_orders_for_user
except ImportError:
    print("Could not import email parser")

class Command(BaseCommand):
    help = 'Sync emails for all users or specific user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of specific user to sync'
        )

    def handle(self, *args, **options):
        user_email = options.get('user_email')
        
        if user_email:
            # Sync specific user
            try:
                user = User.objects.get(email=user_email)
                self.stdout.write(f'Syncing emails for {user.email}...')
                parse_orders_for_user(user.email)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully synced emails for {user.email}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {user_email} not found')
                )
        else:
            # Sync all users
            users = User.objects.filter(is_active=True)
            self.stdout.write(f'Syncing emails for {users.count()} users...')
            
            for user in users:
                try:
                    self.stdout.write(f'Syncing {user.email}...')
                    parse_orders_for_user(user.email)
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error syncing {user.email}: {e}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS('Email sync completed for all users')
            )
