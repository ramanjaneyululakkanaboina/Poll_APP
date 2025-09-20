from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "print hello message"

    def add_arguments(self, parser):
        parser.add_argument('arg_name', type=str, help='Description of the argument')
        parser.add_argument('--optional_flag', action='store_true', help='An optional flag')
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Helo, THis is Ram"))

        arg_value = options['arg_name']
        if options['optional_flag']:
            self.stdout.write(self.style.WARNING(f'optional flag detected for {arg_value}!'))
        else:
            self.stdout.write(self.style.ERROR(f'Executing command with argument: {arg_value}'))

        
