# Django Blog Authentication System

##  Overview
This project implements **user authentication** in Django:
- User Registration
- User Login / Logout
- User Profile Page
- Session-based authentication

##  Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd django_blog

# Blog Post Management (CRUD)

## Features:
- **List Posts**: Anyone can see all blog posts.
- **View Post**: Anyone can view a single post.
- **Create Post**: Only logged-in users can create new posts.
- **Edit/Delete Post**: Only the author of the post can edit or delete it.

## Setup Instructions:
1. Run `python manage.py makemigrations` and `python manage.py migrate`.
2. Add `'blog'` to `INSTALLED_APPS` in `settings.py`.
3. Include blog URLs in project `urls.py`:
   ```python
   path('', include('blog.urls')),