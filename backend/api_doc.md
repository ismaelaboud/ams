# SPH Asset Management System (Backend)

## API Endpoints Table

| HTTP Method | Endpoint                            | Description                        | Access        |
| ----------- | ----------------------------------- | ---------------------------------- | ------------- |
| POST        | `/api/auth/register/`               | Register a new user                | Public        |
| POST        | `/api/auth/login/`                  | Login a user and obtain a JWT      | Public        |
| POST        | `/api/auth/token/refresh/`          | Refresh JWT                        | Authenticated |
| POST        | `/api/auth/password-reset/`         | Request password reset             | Public        |
| POST        | `/api/auth/password-reset-confirm/` | Confirm password reset             | Public        |
| GET         | `/api/profile/`                     | Get user profile                   | Authenticated |
| GET         | `/api/assets/`                      | List all assets                    | Authenticated |
| POST        | `/api/assets/`                      | Create a new asset                 | Admin         |
| GET         | `/api/assets/:id/`                  | Retrieve a specific asset          | Authenticated |
| PUT         | `/api/assets/:id/`                  | Update a specific asset            | Admin         |
| DELETE      | `/api/assets/:id/`                  | Delete a specific asset            | Admin         |
| GET         | `/api/categories/`                  | List all categories                | Authenticated |
| POST        | `/api/categories/`                  | Create a new category              | Admin         |
| GET         | `/api/tags/`                        | List all tags                      | Authenticated |
| POST        | `/api/tags/`                        | Create a new tag                   | Admin         |
| GET         | `/api/users/`                       | List all users                     | Admin         |
| POST        | `/api/users/`                       | Create a new user                  | Admin         |
| GET         | `/api/users/:id/`                   | Retrieve a specific user           | Admin         |
| PUT         | `/api/users/:id/`                   | Update a specific user             | Admin         |
| DELETE      | `/api/users/:id/`                   | Delete a specific user and profile | Admin         |
| GET         | `/api/roles/`                       | List all roles                     | Admin         |
| POST        | `/api/roles/`                       | Create a new role                  | Admin         |
| GET         | `/api/departments/`                 | List all departments               | Admin         |
| POST        | `/api/departments/`                 | Create a new department            | Admin         |
| GET         | `/api/requests/`                    | List all asset requests            | Admin         |
| POST        | `/api/requests/`                    | Request an asset                   | Authenticated |
| PUT         | `/api/requests/:id/approve/`        | Approve an asset request           | Admin         |
| PUT         | `/api/requests/:id/deny/`           | Deny an asset request              | Admin         |
| GET         | `/api/requests/:id/access/`         | Access an approved asset           | Authenticated |

## API Visual Representation

+------------------+    +---------------------+    +-----------------+
|     Client       |    |      Frontend       |    |   Authentication|
|                  |    |      Next.js        |    |     JWT/DRF     |
+------------------+    +---------------------+    +-----------------+
         |                        |                      |
         |                        |                      |
         |        HTTP Request    |                      |
         |<---------------------->|                      |
         |                        |                      |
         |                        |                      |
+------------------+    +---------------------+    +-----------------+
|    Asset API     |    |    User API         |    |  Authentication |
|    Endpoints     |    |    Endpoints        |    |  Endpoints      |
|  - /assets       |    |  - /users           |    |  - /auth/login  |
|  - /assets/:id   |    |  - /users/:id       |    |  - /auth/register|
|  - /categories   |    |  - /roles           |    |  - /auth/password-reset|
|  - /tags         |    |  - /departments     |    |  - /auth/password-reset-confirm|
+------------------+    +---------------------+    +-----------------+
         |                        |
         |                        |
         |                        |
+------------------+    +---------------------+    +-----------------+
|   Business Logic |    |    Data Access      |    |  Authentication |
|      Services    |    |      Layer          |    |  Layer          |
+------------------+    +---------------------+    +-----------------+
         |                        |
         |                        |
         |                        |
+------------------+    +---------------------+    +-----------------+
|   Asset Model    |    |     Profile         |    |   User Model    |
|  - id            |    |  - id               |    |  - id           |
|  - name          |    |  - user             |    |  - username     |
|  - asset_type    |    |  - role             |    |  - password     |
|  - description   |    |  - department       |    |  - email        |
|  - serial_number |    |                     |    |  - first_name   |
|  - category_id   |    |                     |    |  - last_name    |
|  - tags (M2M)    |    |                     |    +-----------------+
|  - assigned_to   |    |                     |
|  - assigned_department |                     |
|  - date_recorded |    |                     |
|  - status        |    |                     |
+------------------+    +---------------------+
         |                        |
         |                        |
         |                        |
+------------------------------------------------------------+
|                       PostgreSQL Database                  |
|                                                            |
|  Tables:                                                   |
|  - assets                                                  |
|  - categories                                              |
|  - tags                                                    |
|  - custom_user                                             |
|  - profiles                                                |
|  - roles                                                   |
|  - departments                                             |
+------------------------------------------------------------+
         |
         |
         |
+------------------+
|      Redis       |
|    Cache Layer   |
|  - Cache frequently |
|  - accessed data   |
+------------------+



## Explanation of Visual Representation

1. **Client**: Represents the user interacting with the frontend application.
2. **Frontend (Next.js)**: The frontend application built using Next.js, sending HTTP requests to the backend API endpoints.
3. **Authentication (JWT/DRF)**: Handles user authentication using JSON Web Tokens (JWT) with Django REST Framework (DRF).
4. **API Endpoints**: Detailed endpoints for managing assets, users, roles, authentication, etc.
5. **Business Logic**: Layer where core business logic is implemented.
6. **Data Access Layer**: Layer that handles interactions with the PostgreSQL database.
7. **Database Models**: Represents the structure and relationships of database tables (assets, categories, tags, users, profiles, roles, departments).
8. **Redis Cache Layer**: Caching frequently accessed data to improve performance.

# Database Schema Representation

## Profile Table

| Field         | Data Type | Description                              |
|---------------|-----------|------------------------------------------|
| id (PK)       | Integer   | Primary key                              |
| user_id (FK)  | Integer   | Reference to Django User model (`CustomUser`) |
| role          | String    | User role (`admin`, `user`, `manager`)   |
| department    | String    | Department assigned to the user          |
| ...           | ...       | Other profile fields as needed           |

## Asset Table

| Field               | Data Type | Description                              |
|---------------------|-----------|------------------------------------------|
| id (PK)             | Integer   | Primary key                              |
| name                | String    | Asset name                               |
| asset_type          | String    | Type of asset                            |
| description         | Text      | Asset description                        |
| serial_number       | String    | Serial number for unique identification |
| category_id (FK)    | Integer   | Reference to Category model              |
| assigned_to_id (FK) | Integer   | Reference to User model (`CustomUser`) (nullable) |
| assigned_department| String    | Department assigned to the asset         |
| date_recorded       | DateTime  | Timestamp when asset record was created  |
| status              | Boolean   | Asset status (`True` or `False`)         |
| ...                 | ...       | Other asset fields as needed             |

## Category Table

| Field         | Data Type | Description                              |
|---------------|-----------|------------------------------------------|
| id (PK)       | Integer   | Primary key                              |
| name          | String    | Category name                            |

## Tag Table

| Field         | Data Type | Description                              |
|---------------|-----------|------------------------------------------|
| id (PK)       | Integer   | Primary key                              |
| name          | String    | Tag name                                 |

## AssetAssignment Table

| Field                  | Data Type | Description                              |
|------------------------|-----------|------------------------------------------|
| id (PK)                | Integer   | Primary key                              |
| asset_id (FK)          | Integer   | Reference to Asset model                 |
| user_id (FK)           | Integer   | Reference to User model (`CustomUser`)   |
| assigned_to_id (FK)    | Integer   | Reference to Profile model               |
| assigned_department_id | Integer   | Reference to Department model            |
| date_assigned          | Date      | Date when the asset was assigned         |
| return_date            | Date      | Expected return date (nullable)          |

Symbols:
- `(PK)`: Primary Key
- `(FK)`: Foreign Key
                          |

Symbols:
- `(FK)`: Foreign Key
- `(M2M)`: Many-to-Many relationship


# Project Structure

.
├── README.md                     # Project documentation file
├── backend                       # Backend directory
│   ├── api_doc.md                # API documentation Markdown file
│   ├── assets                    # App for managing assets
│   │   ├── __init__.py
│   │   ├── __pycache__           # Cached Python bytecode
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── admin.cpython-311.pyc
│   │   │   ├── apps.cpython-311.pyc
│   │   │   ├── models.cpython-311.pyc
│   │   │   └── ...               # Other cached files
│   │   ├── admin.py              # Admin configurations
│   │   ├── apps.py               # App configuration
│   │   ├── migrations            # Database migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__       # Cached migrations
│   │   │       └── __init__.cpython-311.pyc
│   │   ├── models.py             # Database models
│   │   ├── serializers.py        # API serializers
│   │   ├── tests.py              # Unit tests
│   │   ├── views.py              # API views
│   │   └── viewsets.py           # API viewsets
│   ├── backend                    # Django project directory
│   │   ├── __init__.py
│   │   ├── __pycache__           # Cached Python bytecode
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── settings.cpython-311.pyc
│   │   │   └── urls.cpython-311.pyc
│   │   ├── asgi.py               # ASGI config
│   │   ├── settings.py           # Django settings
│   │   ├── urls.py               # URL routing
│   │   └── wsgi.py               # WSGI config
│   ├── db.sqlite3                # SQLite database (example)
│   ├── manage.py                 # Django management script
│   ├── requirements.txt          # Python dependencies
│   └── routers.py                # API routers
└── frontend                      # Frontend directory (not shown)
    ├── ...                       # Other frontend files and directories
