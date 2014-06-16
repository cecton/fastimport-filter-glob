#!/usr/bin/env python

import re, sys
import fnmatch
from fastimport import parser
from fastimport.processors import filter_processor


class GlobFilterProcessor(filter_processor.FilterProcessor):
    def pre_process(self):
        if isinstance(self.params.get('include_paths'), basestring):
            self.includes = re.compile(
                fnmatch.translate(self.params['include_paths']))
        else:
            self.includes = self.params.get('include_paths')
        if isinstance(self.params.get('exclude_paths'), basestring):
            self.excludes = re.compile(
                fnmatch.translate(self.params['exclude_paths']))
        else:
            self.excludes = self.params.get('exclude_paths')
        self.squash_empty_commits = bool(
            self.params.get('squash_empty_commits', True))
        # No new root
        self.new_root = None
        # Buffer of blobs until we know we need them: mark -> cmd
        self.blobs = {}
        # These are the commits we've squashed so far
        self.squashed_commits = set()
        # Map of commit-id to list of parents
        self.parents = {}


    def _path_to_be_kept(self, path):
        return ((not self.excludes or not self.excludes.search(path)) and
                (not self.includes or self.includes.search(path)))

if __name__ == '__main__':
    if ('squash_empty_commits' not in
            filter_processor.FilterProcessor.known_params):
        raise Exception("installed python-fastimport does not "
            "support not squashing empty commits. Please install "
            " a newer python-fastimport to use "
            "--dont-squash-empty-commits")

    import argparse
    cmdparser = argparse.ArgumentParser()
    cmdparser.add_argument('--exclude_paths', '-x',
        help="Exclude these paths from commits. (accept globs)")
    cmdparser.add_argument('--include_paths', '-i',
        help="Only include commits affecting these paths. (accept globs)")
    opt = cmdparser.parse_args()

    proc = GlobFilterProcessor(params={
        'exclude_paths': opt.exclude_paths,
        'include_paths' : opt.include_paths,
        'squash_empty_commits': True,
    })
    p = parser.ImportParser(sys.stdin)
    try:
        proc.process(p.iter_commands)
    except IOError, exc:
        sys.stderr.write(str(exc) + "\n")
