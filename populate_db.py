import os
import django
import random
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

from tasks.models import Project, Task
from django.contrib.auth.models import User
def populate_db():
    fake = Faker()

    # Create Projects
    projects = [Project.objects.create(
        name=fake.bs().capitalize(),
        start_date=fake.date_time_this_year()
    ) for _ in range(50)]
    print(f"✅ Created {len(projects)} projects.")

    # Create Employees
    user = [User.objects.create(
        username=fake.user_name(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        password = fake.password()
    ) for _ in range(50)]
    print(f"✅ Created {len(user)} employees.")

    # Define allowed task statuses
    task_statuses = ['PENDING', 'IN-PROCESS', 'COMPLETED']

    # Create Tasks
    tasks = []
    for _ in range(50):
        task = Task.objects.create(
            project=random.choice(projects),
            task_name=fake.sentence(nb_words=4),
            description=fake.paragraph(),
            due_date=fake.date_this_year(),
            status=random.choice(task_statuses),
            is_completed=random.choice([True, False])
        )
        assigned_user = random.sample(user, random.randint(1, 3))
        task.assigne_to.set(assigned_user)
        tasks.append(task)

    print("✅ Populated TaskDetails for all tasks.")
    print("🎉 Database populated successfully!")

populate_db()
