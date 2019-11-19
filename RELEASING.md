# Release Checklist

- [ ] Get master to the appropriate code release state.
      [Travis CI](https://travis-ci.org/SethMMorton/natsort) cleanly for all merges to
      master.
      [![Build Status](https://travis-ci.org/SethMMorton/natsort.svg?branch=master)](https://travis-ci.org/SethMMorton/natsort)

- [ ] Tag with the version number:

```bash
git tag -a 6.3.0
```

- [ ] Push tag:

```bash
git push --tags
```

- [ ] Check the tagged [Travis CI build](https://travis-ci.org/SethMMorton/natsort) has
      deployed to [PyPI](https://pypi.org/project/natsort/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y natsort && pip3 install -U natsort
```
