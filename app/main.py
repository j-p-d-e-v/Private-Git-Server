from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.GitRepo import GitRepo
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
def repositories(search: str = None, branch: str = "master", commits_limit: int = 1):
    git_repo = GitRepo()
    repos = git_repo.listRepos(search=search,branch=branch,commits_limit=commits_limit)
    return repos

@app.get("/repository")
def repository(repo_name: str, branch: str = "master", commits_limit: int = 3):
    git_repo = GitRepo()
    repos = git_repo.getRepo(repo_name=repo_name,branch=branch,commits_limit=commits_limit)
    return repos

class CreateRepo(BaseModel):
    name: str

class DeleteRepo(BaseModel):
    name: str

class RenameRepo(BaseModel):
    current_name: str
    new_name: str


@app.get("/commit-history")
def commit_history(repo_name:str, branch: str = "master", commits_limit:int = 3):
    try:
        git_repo = GitRepo()
        return git_repo.commitHistory(repo_name,branch,commits_limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/commit-changes")
def commit_changes(repo_name:str, commit_hash:str):
    try:
        git_repo = GitRepo()
        return git_repo.commitDiff(repo_name,commit_hash)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/is-repo-exists")
def is_repo_exists(repo_name:str):
    try:
        git_repo = GitRepo()
        return git_repo.isRepoExists(repo_name)
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