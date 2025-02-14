# DevDash

DevDash is a personalized project tracking dashboard for developers. With DevDash, you can log in with your GitHub account, add repositories you’re actively working on (using the "owner/repo" format), and view enriched insights about each project—such as stars, forks, open issues, and detailed latest commit information across all branches. In-memory caching with `cachetools` is used to speed up repeated API calls.

---

## Features

- **GitHub OAuth Authentication:**  
  Securely log in with your GitHub account using OAuth.

- **Personalized Dashboard:**  
  Track your projects by adding repositories in a single input field (format: `owner/repo`).

- **Enriched Repository Insights:**  
  View key metrics:

  - Star count, forks, and open issues
  - Latest commit details (date and message) across all branches

- **Project Management:**  
  Easily add and remove projects.

- **In-Memory Caching:**  
  Uses `cachetools` to cache GitHub API responses, reducing latency and API usage.

---

## Tech Stack

- **Backend:** FastAPI
- **Frontend:** Jinja2 Templates (with basic styling)
- **Authentication:** GitHub OAuth (via Authlib)
- **Database:** SQLite (using SQLAlchemy)
- **Caching:** Python `cachetools`
- **Deployment:** Ready for deployment on Render (or any Python-compatible platform)

---

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/DevDash.git
   cd DevDash
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   _Ensure your `requirements.txt` includes the following packages:_

   ```txt
   fastapi
   uvicorn
   jinja2
   requests
   sqlalchemy
   authlib
   python-dotenv
   itsdangerous
   cachetools
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the project root with:

   ```env
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   BASE_URL=http://localhost:8000
   ```

   Replace placeholders with your actual GitHub OAuth app credentials. Ensure your GitHub OAuth App's callback URL is set to `http://localhost:8000/auth`.

5. **Run the Application:**
   ```bash
   uvicorn main:app --reload
   ```
   Visit [http://localhost:8000](http://localhost:8000) to begin.

---

## Project Structure

```
DevDash/
├── auth.py              # GitHub OAuth integration
├── config.py            # Configuration and environment variables
├── database.py          # Database connection (SQLAlchemy)
├── main.py              # Main application with routes and caching logic
├── models.py            # Database models (Users and Projects)
├── requirements.txt     # Python dependencies
└── templates/
    ├── base.html        # Base layout template
    ├── index.html       # Landing page template
    ├── dashboard.html   # Dashboard view with project insights
    └── add_project.html # Form for adding new projects
```

---

## Future Enhancements

- **UI/UX Improvements:**
  Enhance the look and feel with a modern CSS framework like Tailwind CSS or Bootstrap.

- **Additional Insights:**
  Further analytics (commit history graphs, contributor stats, etc.).

- **Improved Error Handling:**
  Better user feedback and error management.

---

## Initial Commit Message

Below is the commit message that reflects the current stage of the project:

```
feat: Initial implementation of DevDash

- Added GitHub OAuth authentication using Authlib.
- Implemented a dashboard for tracking user projects with enriched insights
  (stars, forks, open issues, and latest commit info across all branches).
- Enabled project addition via a single "owner/repo" input field.
- Included in-memory caching using cachetools for optimizing GitHub API calls.
- Created project structure, basic routes, and templates.
- Provided comprehensive setup instructions in the README.md.
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---
