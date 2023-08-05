# Broke: Smooth broken link checker for git repositories

If it ain't `broke`, don't fix it. This is a tiny and simple tool to find broken
links in your `git` repositories. Install it with

```bash
pip install broke
```

Then from the base of any git repo simply type

```bash
broke
```

to see all broken links referenced in all files of a directory tracked by `git`, excluding the
files in your `.gitignore`. Get help using `broke --help`.
