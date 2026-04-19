# StudySync

StudySync is a web platform for students where they can create subject-based study groups, join existing groups, and find study buddies for collaborative learning.

## Team

- Davletov Akylbek — Frontend
- Ongarova Nurila — Backend
- Toleubek Alan — Frontend / Integration

## Project Idea

The goal of StudySync is to make it easier for students to find classmates for studying together. Users can register, browse available study groups, create their own groups, join other groups, and manage participation.

## Main Features

- User registration and login
- JWT authentication
- View all study groups
- Create a new study group
- Edit and delete your own study group
- Join a group
- Leave a group
- Remove group members as a group creator
- View available subjects

## Tech Stack

### Frontend

- Angular
- TypeScript
- HttpClient
- Angular Routing
- FormsModule with `[(ngModel)]`

### Backend

- Django
- Django REST Framework
- JWT authentication
- django-cors-headers
- SQLite

## Project Structure

- `frontend/` — Angular client application
- `backend/` — Django + DRF server application

## Main Frontend Files

- `frontend/src/app/app.routes.ts`
- `frontend/src/app/app.html`
- `frontend/src/app/app.scss`
- `frontend/src/app/services/auth.service.ts`
- `frontend/src/app/services/groups.service.ts`
- `frontend/src/app/services/subjects.service.ts`
- `frontend/src/app/interceptors/auth.interceptor.ts`
- `frontend/src/app/guards/auth.guard.ts`
- `frontend/src/app/pages/login-page.component.ts`
- `frontend/src/app/pages/register-page.component.ts`
- `frontend/src/app/pages/groups-page.component.ts`
- `frontend/src/app/pages/group-form-page.component.ts`
- `frontend/src/app/pages/group-detail-page.component.ts`

## Main Backend Files

- `backend/manage.py`
- `backend/config/settings.py`
- `backend/config/urls.py`
- `backend/core/models.py`
- `backend/core/serializers.py`
- `backend/core/views.py`
- `backend/core/urls.py`
- `backend/core/admin.py`
- `backend/core/tests.py`

## Backend Models

- `Subject`
- `StudyGroup`
- `Membership`
- `Category`

## API Endpoints

- `POST /api/login/`
- `POST /api/register/`
- `POST /api/logout/`
- `GET /api/subjects/`
- `GET /api/groups/`
- `POST /api/groups/`
- `GET /api/groups/<id>/`
- `PUT /api/groups/<id>/`
- `DELETE /api/groups/<id>/`
- `POST /api/groups/<id>/join/`
- `POST /api/groups/<id>/leave/`
- `POST /api/groups/<id>/remove-member/`

## How to Run the Project

### Backend

```bash
cd "C:\Users\Asus\OneDrive\Рабочий стол\SS FINAL\StudySync"
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py runserver
```

Backend runs at:

`http://127.0.0.1:8000`

### Frontend

```bash
cd "C:\Users\Asus\OneDrive\Рабочий стол\SS FINAL\StudySync\frontend"
npm install
npm start
```

Frontend runs at:

`http://localhost:4200`

## Demo Flow

1. Register a new user
2. Log in
3. View the list of study groups
4. Create a new group
5. Open group details
6. Join a group with another user
7. Remove a member as the group creator
8. Log out

## Notes

- Subjects can be created through Django admin or directly in the database.
- The project uses JWT authentication with `Bearer` tokens.
- The database file is located at `backend/db.sqlite3`.
