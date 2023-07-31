import os

GIT_REPOSITORIES_DIR = os.environ.get("GIT_REPOSITORIES_DIR","/var/git/repositories")
GIT_REPO_BASE_URL = os.environ.get("GIT_REPO_BASE_URL","http://localhost:5080")
ALLOW_REPO_DELETION = os.environ.get("ALLOW_REPO_DELETION",True)