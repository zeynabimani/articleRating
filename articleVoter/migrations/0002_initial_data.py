from django.db import migrations
from django.utils import timezone
from django.contrib.auth.models import User

def create_initial_data(apps, schema_editor):
    Article = apps.get_model('articleVoter', 'Article')
    Rating = apps.get_model('articleVoter', 'Rating')

    # Create users
    User.objects.create_user(username='user1', email='user1@example.com', password='password', last_login=timezone.now())
    User.objects.create_user(username='user2', email='user2@example.com', password='password', last_login=timezone.now())

    # Create articles
    Article.objects.create(
        title='Article 1',
        text='This is the text of the first article.',
        mean_score=0,
        score_calculate_time=timezone.now()
    )
    Article.objects.create(
        title='Article 2',
        text='This is the text of the second article.',
        mean_score=0,
        score_calculate_time=timezone.now()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('articleVoter', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]