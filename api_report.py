from __future__ import absolute_import
import os, subprocess, sys, shlex

from api_crawler import api_crawler, differ


def diff_versions(old_version, new_version, folder):
    subprocess.call(shlex.split("git checkout tags/%s -- %s" % (old_version, folder)), stdout=open(os.devnull, "w"))
    old = api_crawler(folder).get_crawl_dict()
    subprocess.call(shlex.split("git checkout tags/%s -- %s" % (new_version, folder)), stdout=open(os.devnull, "w"))
    new = api_crawler(folder).get_crawl_dict()

    # Reset HEAD to initial state.
    subprocess.call(shlex.split("git checkout HEAD -- %s" % folder), stdout=open(os.devnull, "w"))
    subprocess.call(shlex.split("git reset HEAD -- %s" % folder), stdout=open(os.devnull, "w"))

    # Combine items removed and added into a single text file.
    diff = differ(old, new)
    pretty_diff = "\n".join(diff.get_diff()) + "\n"

    return pretty_diff


if __name__ == "__main__":
    if len(sys.argv) >= 4:
        sys.stdout.write(diff_versions(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print("Please provide an old version, a new version, and a folder to crawl.")
