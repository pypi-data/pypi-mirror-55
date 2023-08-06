import sys
import os
import shutil
import contextlib
import random
import string
import gitlab
from loguru import logger

"""Import from utils.py"""
from .utils import git

"""Import from readme.py"""
from .readme import generate_readme

"""Import from pipelines.py"""
from .pipelines import generate_pipelines

@contextlib.contextmanager
def remember_cwd():
    """This function keep current directory in memory"""
    curdir = os.getcwd()
    try:
        yield
    finally:
        os.chdir(curdir)


@contextlib.contextmanager
def temp_dir():
    """This function create temporary folder"""
    with remember_cwd():
        tmp_dir = '/tmp/{}'.format(randomString())
        os.mkdir(tmp_dir)
        os.chdir(tmp_dir)
        try:
            yield
        finally:
            os.chdir(os.path.join(tmp_dir, '..'))
            shutil.rmtree(tmp_dir)


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def remote_repository_exists(namespace, name):
    """This function veirfy if remote repository exits"""
    with temp_dir():
        remote = 'git@gitlab.com:{}/{}.git'.format(
            namespace,
            name
        )
        try:
            git('clone -n {}'.format(remote), quiet=True)
        except:
            return False
        return True


class Init():
    COMMAND = 'init'

    def write_readme(self, name, namespace):
        """This function verify the git config and generate generic readme"""
        author = ''
        try:
            config_git = git('config --get user.name')
            author = config_git.stdout.decode(
                'ascii').replace('\n', '').strip()
            if author == '':
                raise RuntimeError
        except:
            raise RuntimeError('Please setup your git config.')

        with open('README.md', 'w+') as readme:
            readme.write(generate_readme(
                name,
                namespace,
                name=author
            ))
        git('add README.md')

    def write_pipelines(self):
        """This function generate default pipelines"""
        with open('.gitlab-ci.yml', 'w+') as pipeline:
            pipeline.write(generate_pipelines())
        git('add .gitlab-ci.yml')

    def initialize_git_repository(self, name, namespace):
        """This function initialize local repository with a generic README.md and CHANGELOG.md"""

        # Ensure that CHANGELOG.md is created
        with open('CHANGELOG.md', 'w+'):
            pass

        if (os.access(".git", os.F_OK) == False):
            git('init')
            git('add CHANGELOG.md')

        if (os.access(".gitlab-ci.yml", os.F_OK) == False):
            self.write_pipelines()

        if (os.access("README.md", os.F_OK) == False):
            self.write_readme(name, namespace)

        diff = git('ls-files -s')
        num_lines = sum(1 for line in diff.stdout)

        if (num_lines != 0):
            git('commit -m init')
        else:
            logger.debug('Nothing changed, no commit will be executed')

    def set_git_remote(self, name, namespace):
        """This function define remote origin repository"""
        remote = 'git@gitlab.com:{}/{}.git'.format(
            namespace,
            name,
        )
        try:
            git('remote add origin {}'.format(remote), quiet=True)
        except:
            git_remote = git('remote -v')
            if remote not in git_remote.stdout:
                raise RuntimeError(
                    'remote origin already exists with a different repository : \nExpected:{}\nGot:{}'.format(
                        remote,
                        git_remote.stdout
                    )
                )

    def change_default_branch(self, switch):
        """This function rename local default branch in to develop instead of master"""
        try:
            git(
                'branch -m master {}'.format(switch), quiet=True
            )
        except:
            raise RuntimeError(
                'Failed to define {} as default branch.',
                switch
            )
        else:
            logger.debug(
                'Define {} as default branch',
                switch
            )

    def initialize_remote_repository(self, name, namespace, base):
        """This function initialize the repository on gitlab.com"""
        try:
            git(
                'push --set-upstream origin {}'.format(base), quiet=True
            )
        except:
            raise RuntimeError(
                'Repository {}/{} already exists or you don\'t have permission to create it.',
                namespace,
                name
            )
        else:
            logger.debug(
                'Created repository {}/{}',
                namespace,
                name
            )

    def initialize_switch_branch(self, branch):
        """This function switch to branch {}"""
        try:
            git('checkout -b {}'.format(branch), quiet=True)
        except:
            git('checkout {}'.format(branch), quiet=True)

    @logger.catch
    def __call__(self, parser, args):
        if not remote_repository_exists(args.namespace, args.name):
            self.initialize_git_repository(args.name, args.namespace)
            try:
                self.change_default_branch(args.switch)
                self.set_git_remote(args.name, args.namespace)
                self.initialize_remote_repository(
                    args.name,
                    args.namespace,
                    args.switch
                )
                self.initialize_switch_branch(args.base)
            except Exception as e:
                logger.error(e)
                return

            git('push -u origin {}'.format(args.base))
            self.initialize_switch_branch(args.switch)
        else:
            remote = 'git@gitlab.com:{}/{}.git'.format(
                args.namespace,
                args.name
            )
            logger.info(
                'This repository already exist. Do git clone {}'.format(remote))
