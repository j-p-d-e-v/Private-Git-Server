import os

GIT_REPO_SSL = True if os.environ.get("GIT_REPO_SSL") == "True" else False
GIT_REPOSITORIES_DIR = os.environ.get("GIT_REPOSITORIES_DIR","/var/git/repositories")
GIT_REPO_BASE_URL = os.environ.get("GIT_REPO_BASE_URL","localhost:5080")
ALLOW_REPO_DELETION = True if os.environ.get("ALLOW_REPO_DELETION") == "True" else False