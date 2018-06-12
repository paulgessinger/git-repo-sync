import argparse
import os
import tempfile
import logging
from urllib.parse import urlparse


from git import Repo

from .config import load_config

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", "-c", required=True)
    p.add_argument("--storage-dir")
    p.add_argument("--verbose", "-v", action="store_true")

    args = p.parse_args()

    assert os.path.exists(args.config), "Config file not found"

    config = load_config(args.config)

    logging.basicConfig(format='%(levelname)-8s %(name)s : %(message)s', level=logging.INFO if not args.verbose else logging.DEBUG)


    print(config)

    if args.storage_dir:
        for item in config:
            sync_repo(item, args.storage_dir)
    else:
        with tempfile.TemporaryDirectory() as tmpdir:
            for item in config:
                sync_repo(item, tmpdir)


def _git_url_to_path(url):
    print(url)
    path = urlparse(url).path
    if path.startswith("/"): path = path[1:]
    path = path.replace("/", "_")
    return path


def sync_repo(item, storage_dir):
    logging.debug("storage_dir: %s", storage_dir)

    src_path = os.path.join(storage_dir, _git_url_to_path(item["src"]))
    dest_path = os.path.join(storage_dir, _git_url_to_path(item["dest"]))

    if not os.path.exists(src_path):
        repo = Repo.init(src_path, bare=True)
        repo.create_remote('src', item["src"])
        repo.create_remote('dest', item["dest"])
    else:
        repo = Repo(src_path)

    assert set(map(str, repo.remotes)) == set(("src", "dest"))

    logging.info("Fetching changes from both repositories")
    repo.remotes.src.fetch()
    repo.remotes.dest.fetch()

    for branch in item["branches"]:
        try:
            logging.info("syncing branch %s", branch)
            ref = repo.remotes.src.refs[branch]
            repo.git.push("dest", "refs/remotes/{}:refs/heads/{}".format(ref, branch))
            logging.info("syncing completed")
        except Exception as e:
            logging.error("Error syncing branch %s: %s", str(e))
            raise e

