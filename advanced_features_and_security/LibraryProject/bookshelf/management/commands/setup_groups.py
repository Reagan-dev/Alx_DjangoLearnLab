from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps

class Command(BaseCommand):
    help = 'Creates user groups and assigns permissions.'

    def handle(self, *args, **kwargs):
        Article = apps.get_model('articles', 'Article')
        permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perms in permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_code in perms:
                permission = Permission.objects.get(codename=perm_code, content_type__app_label='articles')
                group.permissions.add(permission)

        self.stdout.write(self.style.SUCCESS("Groups and permissions set up successfully."))