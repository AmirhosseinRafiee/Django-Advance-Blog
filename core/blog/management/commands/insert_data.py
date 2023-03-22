from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from faker import Faker
import random
from accounts.models import Profile
from blog.models import Category, Post

category_list = ["IT", "Programming", "News", "Fun"]

class Command(BaseCommand):
    help = 'inserting dummy data'

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):

        for cat_name in category_list:
            Category.objects.get_or_create(name=cat_name)
        
        category_objects = Category.objects.all()

        for _ in range(4):
            user = get_user_model().objects.create_user(
                email = self.fake.email(),
                password = self.fake.password(length=10, special_chars = True, digits = True, upper_case = True, lower_case = True),
                is_verified = True
                )
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=5)
            profile.save()

        profile_objects = Profile.objects.all()

        for __ in range(20):
            Post.objects.create(
                author = random.choice(profile_objects),
                title = self.fake.text(max_nb_chars=50),
                content = self.fake.paragraph(nb_sentences=10),
                category = random.choice(category_objects),
                status = random.choice([True, False]),
                published_date = self.fake.date_time_between(start_date='-2y', end_date='+2y')
            )
