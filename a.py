import json
import random
from faker import Faker

fake = Faker()

employees = []

for i in range(1, 201):  # 200 employees
    gender = random.choice(['male', 'female'])
    marital_status = random.choice(['married', 'single'])
    position = random.choice(['Manager', 'Accountant', 'Engineer', 'Sales Rep', 'Technician', 'Supervisor'])
    status = random.choice(['Active', 'Inactive'])
    
    employee = {
        "model": "app_1.employee", 
        "fields": {
            "a": fake.lexify(text='??????'),
            "company": 2,
            "department": random.choice(['HR', 'Finance', 'IT', 'Operations', 'Sales']),
            "role": position,
            "date_joined": str(fake.date_this_decade()),

            "first_name": fake.first_name_male() if gender == 'male' else fake.first_name_female(),
            "last_name": fake.last_name(),
            "other_names": fake.first_name(),
            "gender": gender,
            "date_of_birth": str(fake.date_of_birth(minimum_age=22, maximum_age=60)),
            "picture": "Employee_Pictures/default.jpg",
            "pic_link": "/static/img/default.jpg",
            "location": fake.city(),
            "house_code": fake.bothify(text="HSE-###"),
            "marital_status": marital_status,

            # Father
            "father_first_name": fake.first_name_male(),
            "father_last_name": fake.last_name(),
            "father_date_of_birth": str(fake.date_of_birth(minimum_age=45, maximum_age=80)),
            "father_location": fake.city(),
            "father_marital_status": random.choice(['married', 'divorced', 'separated']),
            "father_living_status": random.choice(['alive', 'dead']),
            "father_contact": fake.phone_number(),

            # Mother
            "mother_first_name": fake.first_name_female(),
            "mother_last_name": fake.last_name(),
            "mother_date_of_birth": str(fake.date_of_birth(minimum_age=45, maximum_age=80)),
            "mother_location": fake.city(),
            "mother_marital_status": random.choice(['married', 'divorced', 'separated']),
            "mother_living_status": random.choice(['alive', 'dead']),
            "mother_contact": fake.phone_number(),

            # Contacts
            "email": fake.email(),
            "phone_number": fake.phone_number(),

            # Account
            "position": position,
            "status": status,
            "z_index": random.randint(1, 5),
            "raw_password": "password123",
            "password": "hashed_password",
            "is_active": True,
            "updated_at": str(fake.date_time_this_year()),
            "is_online": random.choice([True, False]),
        }
    }
    employees.append(employee)

with open("employees_fixture.json", "w") as f:
    json.dump(employees, f, indent=2)

print("✅ Fixture generated: employees_fixture.json")
