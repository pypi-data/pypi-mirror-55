import os
import re

from lib.logging import info, warning
from lib.utils import exec, get_repo_name

class Git(object):
    def __init__(self, repo, dir, repo_name, verbose):
        self.dir = dir
        self.repo = repo
        self.repo_name = repo_name
        self.verbose = verbose

        os.environ['PROJECT_NAME'] = repo_name

    def clone(self):
        status = exec('git clone %s %s' % (self.repo, self.dir), verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def fetch(self):
        cmd = 'git fetch'
        if self.verbose:
            cmd += ' -v'

        status = exec(cmd, cwd=self.dir, verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def list_remote_refs(self):
        cmd = 'git ls-remote -h origin'

        refs = []
        status = exec(cmd, cwd=self.dir)
        for line in status.stdout.decode('utf-8').splitlines():
            refs.append(line.split()[1])

        return refs

    def pull(self):
        cmd = 'git pull'
        if self.verbose:
            cmd += ' -v'

        status = exec(cmd, cwd=self.dir, verbose=self.verbose)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))

    def reset_origin_hard(self):
        status = exec('git reset --hard origin/master', cwd=self.dir)

        if status.returncode is not 0:
            raise Exception(status.stderr.decode('utf-8'))