from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.GitRepo import GitRepo
import re
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/repositories")
def repositories(search: str = None):
    git_repo = GitRepo()
    repos = git_repo.listRepos()
    if search:
        return [ repo for repo in repos if re.search(search.lower(),repo.get("name").lower()) ]
    return repos

class CreateRepo(BaseModel):
    name: str

class DeleteRepo(BaseModel):
    name: str

class RenameRepo(BaseModel):
    current_name: str
    new_name: str


@app.get("/commit-history")
def commit_history(repo_name:str):
    try:
        git_repo = GitRepo()
        return git_repo.commitHistory(repo_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/create-repository")
def create_repository(repo: CreateRepo):
    try:
        git_repo = GitRepo()
        return git_repo.createRepo(repo.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/delete-repository")
def delete_repository(repo_name:str):
    try:
        git_repo = GitRepo()
        return git_repo.deleteRepo(repo_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/rename-repository")
def rename_repository(repo: RenameRepo):
    try:
        git_repo = GitRepo()
        return git_repo.renameRepo(repo.current_name,repo.new_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))