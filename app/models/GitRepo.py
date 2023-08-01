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
        pass
    
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

    def listRepos(self,search=None,branch="master",commits_limit=3):
        try:
            '''
                List all git repositories
                Parameters:
                - search - The value to search.
                - branch - The repository branch to target. Default: master
                - commits_limit - The number of commits to get in the commit history
                Returns: The list of repostories.
            '''
            data = []
            repos = os.listdir(GIT_REPOSITORIES_DIR)
            if search:
                repos = [ repo for repo in repos if re.search(search.lower(),repo.lower()) ]
            for repo_name in repos:
                if os.path.isdir(os.path.join(GIT_REPOSITORIES_DIR,repo_name)):
                    data.append(self.getRepo(repo_name,branch,commits_limit))
            return data
        except Exception as e:
            raise Exception(str(e))
    
    def getRepo(self,repo_name,branch="master",commits_limit=5):
        try:
            '''
                Get repository information.
                Parameters:
                - branch - The repository branch to target. Default: master
                - commits_limit - The number of commits to get in the commit history

                Returns: Git repo information
                - name - The name of the repository.
                - url - The url of the repository.
                - branches - Branches available.
                - branch - The selected branch of the repository.
                - history - The commit history.
            '''
            branches = self.getBranches(repo_name)
            return {
                "name": repo_name,
                "url": self.toUrl(repo_name),
                "branches": branches,
                "branch": branch if branches else "",
                "commit_history": self.commitHistory(repo_name,branch,commits_limit)
            }
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
    
    def getBranches(self,repo_name):

        '''
            Get the repository branches
            Parameters:
            - repo_name - The repository name.    

            Returns: List of branches
        '''
        try:
            if repo_name is None:
                raise Exception("Repository is required.")
            data = []
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)

            if not os.path.exists(repo_path):
                raise Exception("Repository does not exists.")

            repo = git.Repo(repo_path)
            return [head.name for head in repo.heads]
        except Exception as e:
            raise Exception(str(e))
    
    def commitHistory(self,repo_name, branch="master",commits_limit=0):
        try:
            if repo_name is None:
                raise Exception("Repository is required.")
            data = []
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)

            if not os.path.exists(repo_path):
                raise Exception("Repository does not exists.")

            repo = git.Repo(repo_path)
            try:
                for commit in repo.iter_commits(branch,max_count=commits_limit):
                    data.append({
                        "hash": commit.hexsha,
                        "author": commit.author.name,
                        "email": commit.author.email,
                        "date": commit.authored_datetime,
                        "message": commit.message,
                        "branch": branch
                    })
                return data
            except Exception as e:
                print(str(e))
                return []
        except Exception as e:
            raise Exception(str(e))
        

    def getChangeType(self,change):
        '''
            Get the type of change happened in a commit.
            Parameter:
            - change - The change object from commit.diff()

            Returns: The type of change
            - M - Modified
            - D - Deleted
            - A - Added
        '''
        if change.a_path and change.b_path:
            return 'M'
        elif change.a_path:
            return 'D'
        else:
            return 'A'
    
    def commitDiff(self,repo_name, commit_hash):
        try:
            '''
                Get the changes in a commit.

                Parameters:
                - repo_name - The repository name.
                - commit_hash - The commit hash to check for changes.

                Returns: List of changes
                - diff - The changes for each files affected.
                - change_type - The type of change.
            '''
            if repo_name is None:
                raise Exception("Repository is required.")
            data = []
            repo_path = os.path.join(GIT_REPOSITORIES_DIR,repo_name)

            if not os.path.exists(repo_path):
                raise Exception("Repository does not exists.")

            repo = git.Repo(repo_path)
            commit = repo.commit(commit_hash)
            parent_commit = commit.parents[0] if commit.parents else None
            if parent_commit:
                changes = commit.diff(parent_commit,create_patch=True)
                data = []
                if changes:
                    for change in changes:
                        data.append({
                            "current_commit": commit_hash,
                            "previous_commit": parent_commit.hexsha,
                            "change_type": self.getChangeType(change),
                            "diff": change.diff
                        })
                return data
            else:
                return []
        except Exception as e:
            raise Exception(str(e))