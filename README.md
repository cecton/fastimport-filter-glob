fastimport-filter-glob
======================

Command-line script and Python library to use glob to filter files in a
fastimport stream

```bash
# transform a bazaar repository to git but do not add .git directories
# committed by mistake
$ bzr fast-export /path/to/some/repo | \
    fastimport-filter-glob.py -x '*/.git/*' | git fast-import
```
