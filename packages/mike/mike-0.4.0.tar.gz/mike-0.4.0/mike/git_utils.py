# This file is based on the ghp-import package released under
# the Tumbolia Public License.

#                            Tumbolia Public License

# Copyright 2013, Paul Davis <paul.joseph.davis@gmail.com>

# Copying and distribution of this file, with or without modification, are
# permitted in any medium without royalty provided the copyright notice and
# this notice are preserved.

# TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

#   0. opan saurce LOL

from __future__ import division, unicode_literals

import os
import re
import subprocess as sp
import sys
import time
import unicodedata

from enum import Enum
from six import binary_type, text_type

BranchStatus = Enum('BranchState', ['even', 'ahead', 'behind', 'diverged'])


class GitError(OSError):
    pass


class GitBranchDiverged(GitError):
    def __init__(self, branch1, branch2):
        GitError.__init__(self, '{} has diverged from {}'.format(
            branch1, branch2
        ))


class GitRevUnrelated(GitError):
    def __init__(self, branch1, branch2):
        GitError.__init__(self, '{} is unrelated to {}'.format(
            branch1, branch2
        ))


def git_path(path):
    path = os.path.normpath(path)
    # Fix unicode pathnames on macOS; see
    # <http://stackoverflow.com/a/5582439/44289>.
    if sys.platform == 'darwin':  # pragma: no cover
        if isinstance(path, binary_type):
            path = path.decode('utf-8')
        path = unicodedata.normalize('NFKC', path)
    return '/'.join(path.split(os.path.sep))


def make_when(timestamp=None):
    if timestamp is None:
        timestamp = int(time.time())
    timezone = '{:+05d}'.format(-1 * time.timezone // 3600 * 100)
    return '{} {}'.format(timestamp, timezone)


def get_config(key):
    cmd = ['git', 'config', key]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    if p.wait() != 0:
        raise GitError('error getting config: {}'.format(stderr))
    return stdout.strip()


def get_latest_commit(rev, short=False):
    cmd = ['git', 'rev-parse'] + (['--short'] if short else []) + [rev]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    if p.wait() != 0:
        raise GitError('error getting latest commit: {}'.format(stderr))
    return stdout.strip()


def has_branch(branch):
    try:
        get_latest_commit(branch)
        return True
    except GitError:
        return False


def get_merge_base(rev1, rev2):
    cmd = ['git', 'merge-base', rev1, rev2]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    result = p.wait()

    if result == 0:
        return stdout.strip()
    elif result == 1:
        raise GitRevUnrelated(rev1, rev2)
    raise GitError('error getting merge-base: {}'.format(stderr))


def compare_branches(branch1, branch2):
    base = get_merge_base(branch1, branch2)
    latest1 = get_latest_commit(branch1)
    latest2 = get_latest_commit(branch2)

    if base == latest1:
        return BranchStatus.even if base == latest2 else BranchStatus.behind
    else:
        return BranchStatus.ahead if base == latest2 else BranchStatus.diverged


def update_ref(branch, new_ref):
    cmd = ['git', 'update-ref', 'refs/heads/{}'.format(branch), new_ref]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stderr = p.communicate()[1]
    if p.wait() != 0:
        raise GitError('error updating ref: {}'.format(stderr))


def try_rebase_branch(remote, branch, force=False):
    remote_branch = '{}/{}'.format(remote, branch)
    if not has_branch(remote_branch):
        return

    if force or not has_branch(branch):
        update_ref(branch, get_latest_commit(remote_branch))
    else:
        status = compare_branches(branch, remote_branch)
        if status == BranchStatus.behind:
            update_ref(branch, get_latest_commit(remote_branch))
        if status == BranchStatus.diverged:
            raise GitBranchDiverged(branch, remote_branch)


class FileInfo(object):
    def __init__(self, path, data, mode=0o100644):
        self.path = path
        self.data = data
        self.mode = mode

    def __eq__(self, rhs):
        return (self.path == rhs.path and self.data == rhs.data and
                self.mode == rhs.mode)

    def __repr__(self):
        return '<FileInfo({!r}, {:06o})>'.format(self.path, self.mode)

    def copy(self, destdir='', start=''):
        return FileInfo(
            os.path.join(destdir, os.path.relpath(self.path, start)),
            self.data, self.mode
        )


class Commit(object):
    def __init__(self, branch, message):
        cmd = ['git', 'fast-import', '--date-format=raw', '--quiet']
        self._pipe = sp.Popen(cmd, stdin=sp.PIPE, universal_newlines=False)
        self._start_commit(branch, message)
        self._finished = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self._finished:
            if exc_type:
                self.abort()
            else:
                self.finish()

    def _write(self, data):
        if isinstance(data, text_type):  # pragma: no branch
            data = data.encode('utf-8')
        return self._pipe.stdin.write(data)

    def _start_commit(self, branch, message):
        name = get_config('user.name')
        email = get_config('user.email')
        self._write('commit refs/heads/{}\n'.format(branch))
        self._write('committer {name} <{email}> {time}\n'.format(
            name=name, email=email, time=make_when()
        ))
        self._write('data {length}\n{message}\n'.format(
            length=len(message), message=message
        ))
        try:
            head = get_latest_commit(branch)
            self._write('from {}\n'.format(head))
        except GitError:
            pass

    def delete_files(self, files):
        if files == '*':
            self._write('deleteall\n')
        else:
            for f in files:
                self._write('D {}\n'.format(f))

    def add_file(self, file_info):
        self._write('M {mode:06o} inline {path}\n'.format(
            path=git_path(file_info.path), mode=file_info.mode
        ))
        self._write('data {}\n'.format(len(file_info.data)))
        self._write(file_info.data)
        self._write('\n')

    def finish(self):
        if self._finished:
            raise GitError('commit already finalized')
        self._finished = True

        self._write('\n')
        self._pipe.stdin.close()
        if self._pipe.wait() != 0:  # pragma: no cover
            raise GitError('failed to process commit')

    def abort(self):
        if self._finished:
            raise GitError('commit already finalized')
        self._finished = True

        self._pipe.stdin.close()
        self._pipe.terminate()
        self._pipe.wait()


def push_branch(remote, branch, force=False):
    cmd = (['git', 'push'] + (['--force'] if force else []) +
           ['--', remote, branch])
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    if p.wait() != 0:
        raise GitError('failed to push branch: {}'.format(stderr))


def file_mode(branch, filename):
    filename = filename.rstrip('/')
    # The root directory of the repo is, well... a directory.
    if not filename:
        return 0o040000

    cmd = ['git', 'ls-tree', '--', branch, git_path(filename)]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    if p.wait() != 0:
        raise GitError('unable to read file: {}'.format(stderr))
    if not stdout:
        raise GitError('file not found')

    return int(stdout.split(' ', 1)[0], 8)


def read_file(branch, filename, universal_newlines=False):
    cmd = ['git', 'show', '{branch}:{filename}'.format(
        branch=branch, filename=git_path(filename)
    )]
    p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE,
                 universal_newlines=universal_newlines)
    stdout, stderr = p.communicate()
    if p.wait() != 0:
        raise GitError('unable to read file: {}'.format(stderr))
    return stdout


def walk_files(branch, path=''):
    cmd = ['git', 'ls-tree', '-r', '--', '{branch}:{path}'.format(
        branch=branch, path=path
    )]
    with open(os.devnull, 'wb') as devnull:
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=devnull,
                     universal_newlines=True)

        for line in p.stdout:
            strmode, _, _, filename = re.split(r'\s', line.rstrip(), 3)
            mode = int(strmode, 8)
            filepath = os.path.join(path, os.path.normpath(filename))
            yield FileInfo(filepath, read_file(branch, filepath), mode)

        p.stdout.close()
        if p.wait() != 0:
            # It'd be nice if we could read from stderr, but it's somewhat
            # complex to do that while avoiding deadlocks. (select(2) does this
            # on POSIX systems, but that doesn't work on Windows.)
            raise GitError('unable to read files')


def walk_real_files(srcdir):
    for path, _, filenames in os.walk(srcdir):
        for f in filenames:
            filepath = os.path.join(path, f)
            mode = 0o100755 if os.access(filepath, os.X_OK) else 0o100644
            with open(filepath, 'rb') as fd:
                data = fd.read()
            yield FileInfo(filepath, data, mode)
