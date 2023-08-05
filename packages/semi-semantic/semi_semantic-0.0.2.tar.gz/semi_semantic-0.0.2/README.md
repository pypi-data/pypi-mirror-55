semi-semantic
=============

A Python library for parsing/formatting/comparing semi-semantic versions.

Ported from Ruby version: https://github.com/pivotal-cf-experimental/semi_semantic

Why not just use Semantic Versioning?
-------------------------------------

The purpose of this library is to _support, but not require_ semantic versioning.

How is this different than Semantic Versioning?
-----------------------------------------------

Unlike SemVer, Semi-Semantic does not define exactly how it must be used.

Semi-Semantic...

- Allows unlimited version segment components separated by periods (accessed by array index).
  - Does not have named concept of 'major', 'minor', or 'patch' versions.
- Supports underscores, to allow compatibility with ruby gem conventions and timestamps.

Usage
-----

```python
import semi_semantic.Version
...
version_string = "1.0.2-alpha.1+build.10"
version = semi_semantic.Version.parse(version_string)

print(version.release)
# '1.0.2'

print(version.pre_release)
# 'alpha.1'

print(version.post_release)
# 'build.10'

# increment post-release number
print(semi_semantic.Version(version.release, version.pre_release, version.post_release.increment()))
# '1.0.2-alpha.1+build.11'

# increment pre-release number
print(semi_semantic.Version(version.release, version.pre_release.increment()))
# '1.0.2-alpha.2'

# increment release number
print(semi_semantic.Version(version.release.increment()))
# '1.0.3'

# increment 'major' release number
print(semi_semantic.Version(version.release.increment(0)))
# '2.0.0'

# increment 'minor' release number
print(semi_semantic.Version(version.release.increment(1)))
# '1.1.0'

# increment second most least significant release number
print(semi_semantic.Version(version.release.increment(-2)))
# '1.1.0'

```
