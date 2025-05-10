# Fitness Management System 🏋️‍♂️

A Flask-based RESTful API for managing a fitness platform.
The system allows users to sign up, subscribe to plans, 
access exercises, and track progress, with separate roles 
for admins, trainers, and clients.

## 🔧 Technologies Used

- **Python 3.11**
- **Flask** (RESTful API)
- **PostgreSQL** (SQLAlchemy)
- **Marshmallow** (data validation)
- **AWS S3** (media storage)
- **PayPal SDK** (subscription payments)

## 🎯 Features

-  User registration & authentication (with hashed passwords)
-  Role-based access control (`Admin`, `Trainer`, `Clients`)
-  Trainers can create and delete exercises and programs
-  Clients can view assigned programs and exercises
-  Image/video support using Base64 and AWS S3
-  PayPal payment integration
-  Unit testing with mocking
-  RESTful routing and input validation

## 🧪 Testing

The project includes unit and integration 
tests for resources like exercises, users, 
and programs. **Factory Boy and Flask-Testing** 
are used for mock data and test client setup.

To run the tests use:
```bash
pytest
```

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/fitness-system.git
cd fitness-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a .env file with your database and other credentials

```bash
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_PORT=5432
DB_NAME=fitness_system
TEST_DB_NAME=fitness_system_testing
SECRET_KEY=your_secret_key
AWS_ACCESS_KEY=aws_secret_key
AWS_SECRET=aws_secret
AWS_BUCKET=yuor_aws_bucket
AWS_REGION=aws_region
CLIENT_ID=paypal_client_id
PAYPAL_SECRET=paypal_secret_key
CLIENT_URL="http://127.0.0.1:5000"
```

## 📄 License
This project is **not licensed** for commercial use. 
Intended for **educational and demo purposes**.

## 🙋‍♂️ Author
**Anton Milev**
