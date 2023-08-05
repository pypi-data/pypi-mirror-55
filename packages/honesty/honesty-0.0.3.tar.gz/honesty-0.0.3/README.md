# Honesty

There's a long tail of people doing interesting/sketchy things to packages on
pypi.  Most aren't malicious, but this project gives you an easy way to check
for some of the obvious ways that packages might be tampered with.

# Usage

```
honesty list <package name>
honesty check <package name> [version|"*"] [--verbose]
```

It will store a package cache by default under `~/.cache/honesty/pypi` but you
can change that with `HONESTY_CACHE` env var.  If you have a local bandersnatch,
specify `HONESTY_MIRROR_BASE` to your `/simple/` url.


# Exit Status

These are bit flags to make sense when there are multiple problems.  If you pass
`*` for version, they are or'd together.

```
0   if only sdist or everything matches
1   if only bdist
2   (reserved for future "extraction error")
4   some .py from bdist not in sdist
8   some .py files present with same name but different hash in sdist (common
    when using versioneer or 2to3)
```
