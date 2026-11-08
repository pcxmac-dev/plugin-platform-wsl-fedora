# Changelog

## 0.3.0 (2026-11-07)

On liminal-libs 1.26.0 (the user: "each plugin should have a scheme for checking the environment to see if it supports
installing the operating system it has in its name, if the criteria are met according to the O/S, then the install
method should be not locked out, after the install is run a terminal pops up in the plugin and shows the install
progress, after the install is complete, the user can use the plugin to update the environment's packages"; "the plugin
also allows for a user to login through a terminal in to the environment"): `check` (Windows that runs WSL 2, WSL and its
kernel, a WSL that installs under a name of Liminal's, a Fedora on Microsoft's list, the processor, 4 GB free), the install's output
streamed to the platform's terminal panel, `update_packages` (dnf upgrade) and `terminal` (a login shell into it).

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
