# plugin-platform-wsl-fedora

WSL Fedora for Liminal: Fedora in WSL 2 on this Windows PC, set up by the plugin,
with Docker inside, offered to the framework as the Docker instance `wsl-fedora`.

The user's words (2026-11-07): "the platform is the interface for the software/hardware which facilitates the
liminal framework"; "the scope of the plugin is setting up WSL/Ubuntu and supporting docker for the
platform"; "the ubuntu plugin needs to be able to install docker (do everything manually) and allow
different docker instances to support the liminal framework"; "then create a gentoo and fedora plugin as
well, same scope/function".

## What it does

A machine plugin of the platform (`liminal_libs.machines.MachinePlugin`, plugin API 2.2), the library's
`WslDistribution` with this distribution's name and family. Its hooks:

- `present()`: whether the distribution is installed in WSL.
- `status()`: WSL itself, the distribution's state and version, the default user, Docker inside (installed,
  its version, the daemon answering).
- `setup()`: everything, step by step, each reported: WSL itself (`wsl --install --no-distribution`; Windows
  asks to confirm with elevation and may want a restart), `wsl --update`, WSL 2 as the default, the
  distribution (`wsl --install FedoraLinux-NN --name Liminal-Fedora --location <data folder> --no-launch` from Microsoft's list (the newest Fedora there); Docker from Docker's own dnf repository.), `/etc/wsl.conf` with systemd on and the default user `liminal`
  (WSL_FEDORA_USER) made when absent, Docker installed, the engine started and enabled (systemd, else
  OpenRC, else `service`), the user in the docker group. Everything inside runs as root through `wsl -u
  root`, so no password is asked. A step can be run alone: `setup docker`.
- `run(command)`: a command in the distribution.
- `instances()`: the engine as the Docker instance `wsl-fedora`, reached as `wsl -d FedoraLinux-42 docker`,
  Windows paths under `/mnt`; a login file's `[server] instance = wsl-fedora` runs its mail server there, and
  `liminal_libs.docker.instance("wsl-fedora")` gives any app the engine.

Variables: `WSL_FEDORA_DISTRIBUTION` (the WSL name, `Liminal-Fedora` unless said), `WSL_FEDORA_USER`.

Its distribution is Liminal's own, installed beside the user's distributions and never taking one of them: the plugin
is valid only with it installed, and the platform disables it until then.

## From the command line

```
python -m plugin_platform_wsl_fedora status
python -m plugin_platform_wsl_fedora setup            # everything; or: setup docker engine user
python -m plugin_platform_wsl_fedora run -- docker ps
python -m plugin_platform_wsl_fedora instances
```

The platform app drives the same hooks from its page. Nothing here is sent anywhere but Docker's and the
distribution's own download servers, when `setup` installs.

## Its check, its install, its updates, its terminal

`check` says whether this PC can install Liminal-Fedora: Windows that runs WSL 2, WSL installed with its kernel, WSL 2.4.4 or later (the install under a name of Liminal's), a Fedora on Microsoft's list, a processor it is built for (x86-64 or Arm64), 4 GB free on the data folder's drive. The platform's page shows each
criterion and unlocks the install only when every one is met; the install's output shows in a terminal panel as it
runs. Once installed, `update_packages` brings its packages up to date (dnf upgrade) and `terminal` opens a login shell
into it on the page.

## Its services

The user's words (2026-11-08): "lets have, in the WSL plugins, a breakdown of the major services running, the 'scanning function' should be capable of using openrc or systemd to look for init type and differentiate between somewhat trivial processes and major services that are online". `services` scans what runs in Liminal-Fedora, as root, with one script (liminal-libs'
`machines.services`): which init system runs (systemd or OpenRC, or SysV scripts through the service command) and what
PID 1 is; every service it knows with its state; the processes. The major services (Docker, databases, web, mail and
DNS servers, SSH, VPNs, the firewall, Liminal's own apps) are listed with what each is and its memory; a service not
known here is listed with its own description; the system's own (logging, time, devices, D-Bus, logins, package
daemons, the WSL bridge) are counted and named in a note, with any that failed. The platform's page shows the table;
the scan runs only while the distribution runs and is kept 30 s: a status never starts a stopped distribution.

## Its API

The user's words (2026-11-11): "each plugin should reflect the the API its attached to, and present links that provide
documentation, the plugin interface should more or less contain what it already has, BUT, it should also expose more of
what the API is about". Since 0.9.0 (plugin API 2.2) the plugin declares what it attaches to (`apis.py`), and the
platform's page draws each card: what the API is, its links, every part of it (those the plugin uses first, the rest
under "more of the API") and every call it makes, with the API's other notable calls beside them.

- **WSL (wsl.exe)**, Microsoft's: [Basic commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands),
  [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install),
  [wsl.conf and .wslconfig](https://learn.microsoft.com/en-us/windows/wsl/wsl-config),
  [systemd in WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd),
  [releases](https://github.com/microsoft/WSL/releases). The plugin installs Liminal-Fedora with it (the newest
  FedoraLinux-NN on Microsoft's list) and runs everything inside through it; WSL's own record of each install (its Lxss
  registry key, which Microsoft documents no page for) is read to list them, and written only by Rename.
- **DNF**, Fedora's packages: [DNF5's documentation](https://dnf5.readthedocs.io/en/latest/),
  [Using DNF](https://docs.fedoraproject.org/en-US/quick-docs/dnf/), [Fedora in WSL](https://docs.fedoraproject.org/en-US/cloud/wsl/).
  Fedora's pages refuse automated readers (a check page), but answer.
- **Docker Engine**, from Docker's own repository: [Install Docker Engine on Fedora](https://docs.docker.com/engine/install/fedora/),
  [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/),
  [release notes](https://docs.docker.com/engine/release-notes/).
- **systemd**, the install's init: [systemctl(1)](https://www.freedesktop.org/software/systemd/man/latest/systemctl.html):
  the services scan, and Pause (systemd's freezer).

`api_facts()` says what the plugin kept of them while it ran, asking nothing: Microsoft's list as last read and the
newest Fedora on it, Docker inside as last seen, the init the last services scan found. Every address on the cards was
read on 2026-11-11; the test `test_the_cards_pages_answer` asks each of them again when `LIMINAL_VENDOR_PAGES=1` is set
(it is skipped otherwise).
