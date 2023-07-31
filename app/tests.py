from unittest import TestCase
from models.GitRepo import GitRepo
import pprint


class GitRepoTest(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.repo_name = "test-repo----.."
        self.rename_repo_name = "rename-test-r...epo"
    
    def _create_repo(self):
        print("==================================")
        print("_create_repo")
        git_repo = GitRepo()
        repo = git_repo.createRepo(self.repo_name)
        pprint.pprint(repo)
        self.repo_name = repo.get("name")
        self.assertTrue(isinstance(repo,dict),msg="Return data must be a dictionary.")
    
    def _rename_repo(self):
        print("==================================")
        print("_rename_repo")
        git_repo = GitRepo()
        repo = git_repo.renameRepo(self.repo_name,self.rename_repo_name)
        pprint.pprint(repo)
        self.rename_repo_name = repo.get("name")
        self.assertTrue(isinstance(repo,dict),msg="Return data must be a dictionary.")
    
    def _delete_repo(self):
        print("==================================")
        print("_delete_repo")
        git_repo = GitRepo()
        repo = git_repo.deleteRepo(self.rename_repo_name)
        print("delete",repo)
        self.assertTrue(isinstance(repo,dict),msg="Repo must be successfully deleted.")
    
    def _list_repos(self):
        print("==================================")
        print("_list_repos")
        git_repo = GitRepo()
        repos = git_repo.listRepos()
        pprint.pprint(repos)
        self.assertTrue(isinstance(repos,list),msg="Repo must be a list.")

    def test_git_repo(self):
        self._create_repo()
        self._rename_repo()
        self._list_repos()
        self._delete_repo()
    
    def tearDown(self) -> None:
        super().tearDown()
