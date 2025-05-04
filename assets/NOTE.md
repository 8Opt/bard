# 🚀 Services and API Endpoints


## Auth 

| Endpoint         | Method | Purpose                                    |
| :--------------- | :----- | :----------------------------------------- |
| `/auth/register` | POST   | Register a new user                        |
| `/auth/login`    | POST   | Login and receive access/refresh tokens    |
| `/auth/refresh`  | POST   | Refresh access token                       |
| `/auth/logout`   | POST   | Logout and invalidate refresh token        |
| `/auth/me`       | GET    | Get current user profile (protected route) |


## Chat 

| Endpoint        | Method | Purpose                                           |
| :-------------- | :----- | :------------------------------------------------ |
| `/chat/chat`    | POST   | Send a message to the chatbot and receive a reply |
| `/chat/history` | GET    | Retrieve conversation history by session          |
| `/chat/clear`   | POST   | Clear conversation memory by session              |
| `/chat/status`  | GET    | Check chatbot online status                       |