# Changelog

## 0.1.1 (2026-11-07)

The plugin names Docker's repository for Fedora (`docker_repository`), which the library's dnf
recipe fills in (liminal-libs 1.22.1: the library's code names no outside host).

## 0.1.0 (2026-11-07)

The first release: Fedora in WSL 2 set up by the plugin (the library's WslDistribution,
liminal-libs 1.19.0), Docker installed inside by dnf from Docker's own repository, the engine
started and enabled, offered as the Docker instance `wsl-fedora`.
