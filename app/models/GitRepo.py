import git
from settings import GIT_REPOSITORIES_DIR, GIT_REPO_BASE_URL, ALLOW_REPO_DELETION
import os
import shutil
import re

class GitRepo:
    '''Execute git actions'''

    def __init__(self):
        '''
            Initialize the GitRepo class
        '''
    def sanitizeRepoName(self,repo_name):
        repo_name = re.sub(r'[~^.:\\?\[\]*\s]', '-', repo_name)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        if not repo_name or repo_name.startswith('-'):
            raise ValueError("Invalid repository name")
        repo_name = re.sub(r'-{2,}', '-', repo_name)
        return repo_name

    def toUrl(self,repo_name):
        return "{}/{}".format(GIT_REPO_BASE_URL,repo_name)

    def listRepos(self):
        try:
            '''
                List all git repositories
                Returns: The list of repostories.
            '''
            data = []
            for repo_name in os.listdir(GIT_REPOSITORIES_DIR):
                data.append({
                    "name": repo_name,
                    "url": self.toUrl(repo_name)
                })
            return data
        except Exception as e:
            raise Exception(str(e))
    
    def isRepoExists(self,repo_name):
        '''
            Check if repository already exists.
            Parameters:
            - repot_name - The repository to search.

            Returns: The status of the existence of the repo.
            - name - The repo name
            - is_exists - True if exists. False if does not exists.
        '''
        if repo_name is None:
            raise Exception("Repository name is required.")
        
        repos    = os.listdir(GIT_REPOSITORIES_DIR)
        status   =  True if repo_name in repos else False
        return {
            "name": repo_name,
            "is_exists": status
        }
    
    def createRepo(self,repo_name):
        '''
            Create a repository.

            Parameters:
            - repo_name - The repository name.    

            Returns: The name, and url of the repository.
        '''
        try:
            repo_name = self.sanitizeRepoName(repo_name)
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)
            if os.path.exists(repo_path):
                raise Exception("{} already exists.".format(repo_name))

            git.Repo.init(repo_path,bare=True)
            return {
                "name": repo_name,
                "url": self.toUrl(repo_name)
            }
        except Exception as e:
            raise Exception(str(e))
    
    def renameRepo(self,src_repo_name, dst_repo_name):
        '''
            Rename a repository.
            Parameters:
            - src_repo_name - The source repository name.    
            - dst_repo_name - The desired repository name.  

            Returns: The new name, and url of the repository.
        '''
        try:
            src_repo_name = self.sanitizeRepoName(src_repo_name)
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,src_repo_name)
            if not os.path.exists(repo_path):
                raise Exception("Failed to archive repository. {} repository does not exists.".format(src_repo_name))
            dst_repo_name = self.sanitizeRepoName(dst_repo_name)
            dst_repo_path = os.path.join(GIT_REPOSITORIES_DIR,dst_repo_name)
            os.rename(repo_path,dst_repo_path)
            return {
                "name": dst_repo_name,
                "url": self.toUrl(dst_repo_name)
            }
        except Exception as e:
            raise Exception(str(e))

    
    def deleteRepo(self,repo_name):
        '''
            Permanently delete a repository.
            Parameters:
            - repo_name - The repository name.    

            Returns: Throws an exception if failed. True if successfully deleted the repo.
        '''
        try:
            if not ALLOW_REPO_DELETION:
                raise Exception("Deleting of repository is prohibited.")
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)
            if not os.path.exists(repo_path):
                raise Exception("Failed to delete repository. {} repository does not exists.".format(repo_name))
            shutil.rmtree(repo_path)
            return {
                "name": repo_name,
                "deleted": True
            }
        except Exception as e:
            raise Exception(str(e))
        
    
    def commitHistory(self,repo_name):
        try:
            if repo_name is None:
                raise Exception("Repository is required.")
            data = []
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)

            if not os.path.exists(repo_path):
                raise Exception("Repository does not exists.")

            repo = git.Repo(repo_path)
            for commit in repo.iter_commits():
                data.append({
                    "hash": commit.hexsha,
                    "author": commit.author.name,
                    "email": commit.author.email,
                    "date": commit.authored_datetime,
                    "message": commit.message
                })
            return data
        except Exception as e:
            raise Exception(str(e))