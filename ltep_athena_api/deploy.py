import os
from dataclasses import dataclass
from typing import List

import jenkins
from github import Github, enable_console_debug_logging
from github.Repository import Repository
from ltep_athena_api.authenticate import AthenaAuth
from random_word import RandomWords


@dataclass
class DeployGithubAthena:

    def create_github_instance(self, acess_token: str) -> Github:
        """This methods creates a Github instance for repositories hosted on GitHub Inc. 
        :param str acess_token: developer token derived from Github
        :raises Exception: if GitHub authenfication was unsuccessful
        :returns: GitHub instance
        :rtype: Github
        """
        try:
            return Github(acess_token)
        except Exception as e:
            print(e)
            raise Exception(
                "Github Instance could not be created. Check credentials")

    def create_github_instance_password(self, username: str, password: str) -> Github:
        """This methods creates a Github instance for repositories hosted on GitHub Inc. 
        :param str acess_token: developer token derived from Github
        :raises Exception: if GitHub authenfication was unsuccessful
        :returns: GitHub instance
        :rtype: Github
        """
        try:
            return Github(login_or_token=username, password=password)
        except Exception as e:
            print(e)
            raise Exception(
                "Github Instance could not be created. Check credentials")

    def create_github_enterprise_instance(self, base_url: str, login_or_access_token: str):
        """This methods creates a Github instance for repositories hosted on by GitHub enterprise at own server location
        :param str base_url: url location to Github Enterprise 
        :param str acess_token: developer token derived from Github
        :raises Exception: if GitHub authenfication was unsuccessful
        :returns: GitHub instance
        :rtype: Github
        """
        try:
            return Github(
                "https://{hostname}/api/v3".format(base_url), login_or_access_token)
        except Exception as e:
            print(e)
            raise Exception(
                "Github Instance could not be created. Check credentials")

    def get_existing_repo(self, github: Github, repo_full_name_or_repo_id: str) -> Repository:
        """This methods returns a Github Repository for a user
        :param str repo_full_name_or_repo_id: repo's name, e.g. your_github_user/your_repository
        :returns: GitHub instance
        :rtype: Github
        """
        enable_console_debug_logging()
        return github.get_repo(full_name_or_id=repo_full_name_or_repo_id)

    def create_new_github_repo_user(self, github: Github, repo_name: str = 'athena_' + RandomWords().get_random_word(), private: bool = True) -> Repository:
        """This methods creates a Github Repository for a user
        :param Github github: Github instance to perform git operations
        :param str repo_name: repo's name
        :param bool private: private or public repo
        :returns: Repository instance
        :rtype: Repository
        """
        user = github.get_user()
        return user.create_repo(repo_name, private=private)

    def create_new_github_repo_organization(self, github: Github, organization_name: str, repo_name: str = RandomWords().get_random_word(), private: bool = True) -> Repository:
        """This methods creates a Github Repository for a organization
        :param Github github: Github instance to perform git operations
        :param str repo_name: repo's name
        :param bool private: private or public repo
        :returns: Repository instance
        :rtype: Repository
        """
        organization = github.get_organization(organization_name)
        return organization.create_repo(
            repo_name,
            allow_rebase_merge=True,
            auto_init=False,
            private=private,
        )

    def deploy_to_github(self, repo: Repository, folder_location: str):
        """This methods creates a Github Repository for a organization
        :param Github github: Github instance to perform git operations
        :param str repo_name: repo's name
        :param bool private: private or public repo
        :returns: Repository instance
        :rtype: Repository
        """
        listOfFiles = list()
        for (dirpath, dirnames, filenames) in os.walk(folder_location):
            listOfFiles += [os.path.join(dirpath, file) for file in filenames]
        all_files = []
        try:
            contents = repo.get_contents("")
        except Exception as e:
            print(e)
            contents = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace(
                    'ContentFile(path="', '').replace('")', ''))
        try:
            files_to_commit = [trimmed_file.replace("\\", "/")[1:] if len(trimmed_file.split('\\')) > 2 else trimmed_file.replace("\\", "") for trimmed_file in [file.replace(
                folder_location, "") for file in listOfFiles if not '__pycache__' in file and not 'deploy_execution' in file and not 'cpython' in file and not '.git' in file]]
            files_to_commit.append('.gitignore')
            for file_to_commit in files_to_commit:
                with open(folder_location + "/" + file_to_commit, 'r') as file:
                    content = file.read()
                if file_to_commit in all_files:
                    contents = repo.get_contents(file_to_commit)
                    repo.update_file(contents.path, "committing files",
                                     content, contents.sha, branch="master")
                    print(file_to_commit + ' UPDATED')
                else:
                    repo.create_file(file_to_commit, "committing files",
                                     content, branch="master")
                    print(file_to_commit + ' CREATED')
        except Exception as e:
            print(e)
            print('failed_failed: {}'.format(file_to_commit))

    def create_webhook(self, repo: Repository, host: str, endpoint: str = 'github-webhook', events: List[str] = ["push", "pull_request"], active: bool = True):
        """Creates a webhook for the specified repository."""
        config = {
            "url": "http://{host}/{endpoint}/".format(host=host, endpoint=endpoint),
            "content_type": "json"
        }
        try:
            repo.create_hook("web", config, events, active=active)
        except Exception as e:
            print(e)
            raise Exception(
                "GitHub Webhook could have not been created. For more details see error message above.")

    @AthenaAuth.authenticate_access_athena
    def init_default_deployment_user(
            self, github_developer_token: str, repo_full_name_or_repo_id: str, webhook_host: str, folder_location_of_custom_package: str,
            auth: AthenaAuth, create_new_repo: bool = False, new_repo_name: str = None):
        """Creates a webhook for the specified repository.
        :param AthenaAuth auth: AthenaAuth object
        """
        github = self.create_github_instance(
            DeployGithubAthena, acess_token=github_developer_token)
        if create_new_repo:
            if new_repo_name is None:
                repo = self.create_new_github_repo_user(
                    DeployGithubAthena, github=github)
            else:
                repo = self.create_new_github_repo_user(
                    DeployGithubAthena, github=github, repo_name=new_repo_name)
        else:
            repo = self.get_existing_repo(
                DeployGithubAthena, github=github, repo_full_name_or_repo_id=repo_full_name_or_repo_id)
        self.create_webhook(
            DeployGithubAthena, repo=repo, host=webhook_host)


@dataclass
class jenkinsDeploy:

    def connect_to_jenkins(self, host_url: str, user_name: str, password: str) -> jenkins.Jenkins:
        return jenkins.Jenkins(url=host_url, username=user_name, password=password)

    def create_jenkins_job(self, jenkins_server: jenkins.Jenkins, name: str = 'athena_deploy', config_xml: str = jenkins.EMPTY_CONFIG_XML):
        jenkins_server.create_job(name=name, config_xml=config_xml)

    def build_jenkins_job(self, jenkins_server: jenkins.Jenkins, name: str = 'athena_deploy'):
        jenkins_server.build_job(name=name)
