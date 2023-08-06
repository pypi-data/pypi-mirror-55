import configparser
from pathlib import Path
from typing import Optional

import git
import git.exc

# XXX: This is hacky. This should maybe use the Context object or something to
# determine the base directory.


def repo(path: Optional[Path] = None) -> Optional[git.Repo]:
    try:
        r = git.Repo(str(path or Path.cwd()), search_parent_directories=True)
        return r
    except git.exc.InvalidGitRepositoryError:
        return None


# N.B. See https://stackoverflow.com/a/42613047
def user_email(path: Optional[Path] = None) -> Optional[str]:
    r = repo(path)
    if r is None:
        return None
    try:
        return r.config_reader().get_value("user", "email")
    except configparser.NoSectionError:
        return None
    except configparser.NoOptionError:
        return None


def url(path: Optional[Path] = None) -> Optional[str]:
    """Get remote.origin.url for git dir at dirPath"""
    r = repo(path)
    if r and r.remotes and "origin" in r.remotes:
        return r.remotes.origin.url
    else:
        return None


def commit(path: Optional[Path] = None) -> Optional[str]:
    """Get head commit for git dir at dirPath"""
    r = repo()
    if r is None:
        return None
    return str(r.head.commit)
