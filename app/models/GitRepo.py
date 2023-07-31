import git
from settings import GIT_REPOSITORIES_DIR, GIT_REPO_BASE_URL, ALLOW_REPO_DELETION
import os
import shutil

class GitRepo:
    '''Execute git actions'''

    def __init__(self):
        '''
            Initialize the GitRepo class
        '''
    
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
        

    def createRepo(self,repo_name):
        '''
            Create a repository.

            Parameters:
            - repo_name - The repository name.    

            Returns: The name, and url of the repository.
        '''
        try:
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
            - repo_name - The repository name.    

            Returns: The new name, and url of the repository.
        '''
        try:
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,src_repo_name)
            if not os.path.exists(repo_path):
                raise Exception("Failed to archive repository. {} repository does not exists.".format(src_repo_name))
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
            if ALLOW_REPO_DELETION:
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
