# Changelog

## 0.2.0 (2026-11-07)

Its own distribution of Liminal's, Liminal-Fedora, installed beside the user's own and never taking it (the user:
"there are no WSL-liminally scoped installs, so all three WSL plugins are invalid"); the plugin is valid only with it
installed, and the platform disables it until then (liminal-libs 1.24.0: `valid` and `why` in its status).

## 0.1.1 (2026-11-07)

The plugin names Docker's repository for Fedora (`docker_repository`), which the library's dnf
recipe fills in (liminal-libs 1.22.1: the library's code names no outside host).

## 0.1.0 (2026-11-07)

The first release: Fedora in WSL 2 set up by the plugin (the library's WslDistribution,
liminal-libs 1.19.0), Docker installed inside by dnf from Docker's own repository, the engine
started and enabled, offered as the Docker instance `wsl-fedora`.
