# Lucky City API 🏙️

A FastAPI-based REST API that recommends suitable cities for users based on their Four Pillars of Destiny (八字) calculated from their birth date.

## Features ✨

- User authentication with JWT tokens
- Password reset functionality
- City recommendations based on Chinese astrology
- Secure password handling with Argon2
- RESTful API design

## Tech Stack 🛠️

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: JWT
- **Password Hashing**: Argon2
- **AI Integration**: Deepseek API
- **Email**: FastAPI-Mail

## Run Application 🚀

```bash
uvicorn app.main:app --reload
```

## API Endpoints 🛣️

### Authentication
- `POST /users/` - Create new user
- `POST /users/login` - Login user
- `POST /users/forgot-password` - Request password reset
- `POST /users/reset-password-with-token` - Reset password with token

### User Management
- `GET /users/me` - Get current user info
- `PUT /users/reset_password` - Reset password (authenticated)

### Predictions
- `POST /predictions/` - Get city recommendations based on birth date

## License 📄

[MIT License](LICENSE) 