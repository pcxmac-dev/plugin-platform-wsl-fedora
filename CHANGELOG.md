# Changelog

## 0.6.0 (2026-11-09)

The installs' tasks, liminal-libs 1.37.0's (the user: "instead of chosen, put task and for the tasks lets do terminal,
start, pause, stop, allow selection of the linux install by clicking on the list"; "tasks also include uninstall"): a
Fedora install is chosen by a click on its row in the "Fedora installs" table, and above it its tasks: Terminal,
Start (kept running until Stop; a paused one resumed), Pause (its running services frozen by systemd; WSL itself cannot
pause a distribution), Stop… and Uninstall…. Needs liminal-libs>=1.37.0.

## 0.5.0 (2026-11-08)

Every Fedora install listed, and a selector for them (the user: "for the WSL plugins, they need to list all the
'operating systems' that are installed under the plugin's regime, like ubuntu shows all ubuntu installs, fedora --
installs, gentoo -- installs"; "also the ability to uninstall and select which one to terminal in to"; "basically a
selector for different installs"), all of it liminal-libs 1.36.0's: the page's "Fedora installs" table lists every
Fedora distribution installed for this Windows user from WSL's own record (WSL records its flavor (fedora) and version, or a name like FedoraLinux-42), its state, version, WSL, disk and
whose, none started to look. The one chosen (Liminal-Fedora unless another is picked) is the one a terminal opens into,
as its default user, and the one Uninstall unregisters (`wsl --unregister`: its disk deleted for good), one of yours only
after a second confirmation. Needs liminal-libs>=1.36.0.

## 0.4.1 (2026-11-08)

Its icon is Fedora's bubble and its f, drawn in the library's line (liminal-libs 1.33.0's `fedora`; the user: "for the icons, WSL, use the distribution's mascot or icon"). Needs liminal-libs>=1.33.0.

## 0.4.0 (2026-11-08)

Its services (the user: "lets have, in the WSL plugins, a breakdown of the major services running, the 'scanning function' should be capable of using openrc or systemd to look for init type and differentiate between somewhat trivial processes and major services that are online"), on liminal-libs 1.28.0: the platform's page shows what runs in Liminal-Fedora: the
init system found (systemd or OpenRC, or SysV scripts), the major services online with what each is and its memory,
the system's own counted and named in a note; scanned only while the distribution runs, kept 30 s (`services`,
`services(fresh=True)`). A status, the Docker check or the instance list no longer starts a stopped distribution.

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
