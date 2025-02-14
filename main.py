from fastapi import FastAPI, Request, Depends, Form
from starlette.middleware.sessions import SessionMiddleware
from cachetools import TTLCache, cached
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import requests
from sqlalchemy.orm import Session
from datetime import datetime

from auth import router as auth_router
from database import engine, SessionLocal, Base
from models import Project

app = FastAPI()

# Session middleware (replace 'your-secret-key' with a secure key)
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")

# Include auth routes
app.include_router(auth_router)

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency: Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Set up caches: 100 items max, 5 minute TTL (adjust as needed)
repo_cache = TTLCache(maxsize=100, ttl=300)
branches_cache = TTLCache(maxsize=100, ttl=300)
commits_cache = TTLCache(maxsize=200, ttl=300)

@cached(repo_cache)
def get_repo_data(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": f"Failed to fetch repo data: {r.status_code}"}

@cached(branches_cache)
def get_branches(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return {"error": f"Failed to fetch branch data: {r.status_code}"}

@cached(commits_cache)
def get_latest_commit_for_branch(owner: str, repo: str, branch_name: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"sha": branch_name, "per_page": 1}
    r = requests.get(url, params=params)
    if r.status_code == 200:
        commits = r.json()
        if commits:
            commit = commits[0]
            commit_date_str = commit.get("commit", {}).get("author", {}).get("date")
            commit_message = commit.get("commit", {}).get("message")
            return {"date": commit_date_str, "message": commit_message}
    return None

# Landing page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

# Dashboard: Shows user projects with enriched GitHub data
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url="/")
    
    projects = db.query(Project).filter(Project.user_id == user['id']).all()
    project_details = []

    for project in projects:
        owner = str(project.owner)
        repo = str(project.repo)
        
        # Get repository data from cache
        repo_data = get_repo_data(owner, repo)
        
        # Get branches from cache
        branches = get_branches(owner, repo)
        latest_commit = None
        
        if isinstance(branches, list):  # Ensure branches were fetched correctly
            latest_dt = None
            for branch in branches:
                branch_name = branch.get("name")
                if branch_name:
                    commit_info = get_latest_commit_for_branch(owner, repo, branch_name)
                    if commit_info and commit_info.get("date"):
                        try:
                            commit_dt = datetime.strptime(commit_info["date"], "%Y-%m-%dT%H:%M:%SZ")
                        except ValueError:
                            commit_dt = None
                        if commit_dt and (latest_dt is None or commit_dt > latest_dt):
                            latest_dt = commit_dt
                            latest_commit = commit_info
        else:
            latest_commit = {"error": "Failed to fetch branch data"}
        
        project_details.append({
            "id": project.id,
            "owner": owner,
            "repo": repo,
            "stars": repo_data.get("stargazers_count"),
            "forks": repo_data.get("forks_count"),
            "open_issues": repo_data.get("open_issues_count"),
            "latest_commit": latest_commit,
        })
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "projects": project_details})

# GET endpoint for the add project form (separate page)
@app.get("/add-project", response_class=HTMLResponse)
async def add_project_form(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("add_project.html", {"request": request, "user": user})

# POST endpoint to process the form submission
@app.post("/add-project", response_class=HTMLResponse)
async def add_project(request: Request, repo_full: str = Form(...), db: Session = Depends(get_db)):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url="/")
    
    # Expect repo_full in the format "owner/repo"
    if "/" not in repo_full:
        # Optionally, add an error message or flash message
        return RedirectResponse(url="/add-project", status_code=302)
    
    owner, repo = repo_full.split("/", 1)
    owner = owner.strip()
    repo = repo.strip()
    
    new_project = Project(user_id=user['id'], owner=owner, repo=repo)
    db.add(new_project)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)


@app.post("/delete-project/{project_id}")
async def delete_project(request: Request, project_id: int, db: Session = Depends(get_db)):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url="/")
    # Query the project to ensure it belongs to the logged-in user
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == user['id']).first()
    if project:
        db.delete(project)
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)
