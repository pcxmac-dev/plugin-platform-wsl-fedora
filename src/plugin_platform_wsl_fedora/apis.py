"""What WSL Fedora attaches to (plugin API 2.2, liminal_libs.sources.apis; the user, 2026-11-11: "each plugin should
reflect the the API its attached to, and present links that provide documentation ... it should also expose more of
what the API is about"): wsl.exe, Fedora's DNF inside Liminal-Fedora, Docker Engine from Docker's own repository, and
the install's init (systemd). Every address was read on the makers' own pages on 2026-11-11 (`VERIFIED`).

The code that drives them is the library's (liminal_libs.machines.wsl, WslDistribution); the cards are this plugin's:
`facts` says what the plugin kept of them while it ran (asking nothing)."""
from __future__ import annotations

import time

from liminal_libs.sources.apis import Api, Area, Call, Link

VERIFIED = "2026-11-11"
LEARN = "https://learn.microsoft.com/en-us/windows/wsl/"
DOCKER = "https://docs.docker.com/"
SYSTEMD = "https://www.freedesktop.org/software/systemd/man/latest/"
DNF5 = "https://dnf5.readthedocs.io/en/latest/"
KEEP_RUNNING = "wsl -d <distribution> --exec sh -c 'while :; do sleep 3600; done'"

WSL = Api(
    name="WSL (wsl.exe)",
    maker="Microsoft",
    about=("The Windows Subsystem for Linux: Linux distributions running in a light virtual machine on this Windows PC, "
           "installed, listed, started, stopped and removed with wsl.exe, and set up one by one in their /etc/wsl.conf. "
           "The plugin installs Liminal-Fedora with it, runs everything inside Liminal-Fedora through it as root, and "
           "reads WSL's own record of each install to list them without starting one."),
    kind="command",
    base="wsl.exe, windowless (inside a distribution: wsl -d <distribution> --exec ...)",
    version="WSL 2; wsl.exe 2.4.4 or later (wsl --install --name, --location)",
    auth=("none asked: wsl runs as the signed-in Windows user, and `wsl -u root` inside needs no password; installing WSL "
          "itself asks Windows to confirm as an administrator (UAC), and may want a restart"),
    limits=("no request limits (a command on this PC); WSL stops a distribution 15 s after its last session ends "
            "(.wslconfig's instanceIdleTimeout), which is why Start keeps a session open"),
    costs="",
    links=(
        Link("WSL documentation", LEARN, "docs"),
        Link("Basic commands for WSL", LEARN + "basic-commands", "reference"),
        Link("Install WSL", LEARN + "install", "guide"),
        Link("Advanced settings: wsl.conf and .wslconfig", LEARN + "wsl-config", "guide"),
        Link("Use systemd to manage Linux services with WSL", LEARN + "systemd", "guide"),
        Link("Import any Linux distribution", LEARN + "use-custom-distro", "guide"),
        Link("Troubleshooting WSL", LEARN + "troubleshooting", "guide"),
        Link("WSL releases", "https://github.com/microsoft/WSL/releases", "changelog"),
        Link("What's new in WSL, November 2024: wsl --install --name and --location",
             "https://devblogs.microsoft.com/commandline/whats-new-in-the-windows-subsystem-for-linux-in-november-2024",
             "changelog"),
        Link("WSL's source", "https://github.com/microsoft/WSL", "source"),
        Link("WSL in the Microsoft Store", "https://apps.microsoft.com/detail/9P9TQF7MRM4R", "tool"),
    ),
    areas=(
        Area("WSL itself", "installing WSL, updating it, its version and its kernel, its status", LEARN + "install",
             covered="installed and updated by the setup; its version (2.4.4 or later) and its Linux kernel checked first"),
        Area("Distributions from Microsoft's list", "wsl --list --online, then wsl --install <name>, under a name and in a "
             "folder of its own", LEARN + "basic-commands#install",
             covered=("Liminal-Fedora installed from the newest FedoraLinux-NN on the list under its own name, into the "
                      "data folder, not launched")),
        Area("Installed distributions", "each distribution's state and WSL version, the default one",
             LEARN + "basic-commands#list-installed-linux-distributions",
             covered="every Fedora install listed in the installs table, Liminal's and yours, none started to look"),
        Area("Running commands inside", "a command in a distribution, as a user or as root, in a folder",
             LEARN + "basic-commands#run-a-specific-linux-distribution-from-powershell-or-cmd",
             covered="scripts as root on standard input, Docker's checks, the run hook, the terminal"),
        Area("Stopping and removing", "terminating one distribution, shutting WSL down, unregistering a distribution (its "
             "disk deleted)", LEARN + "basic-commands#terminate",
             covered="Stop (wsl --terminate) and Uninstall (wsl --unregister) among an install's tasks"),
        Area("Importing and exporting", "a distribution from a tar file or a disk, and back to one", LEARN + "use-custom-distro"),
        Area("wsl.conf", "a distribution's own settings: [boot] systemd and command, [user] default, automount, network, "
             "interop", LEARN + "wsl-config#wslconf", covered="systemd on and the default user (liminal), written by the setup"),
        Area(".wslconfig", "WSL's settings for every distribution: memory, processors, networking mode, DNS tunneling, "
             "idle timeouts", LEARN + "wsl-config#wslconfig"),
        Area("systemd", "systemd as a distribution's init, turned on in wsl.conf", LEARN + "systemd",
             covered="turned on by the setup; Pause freezes the running services with systemd's freezer"),
        Area("WSL's record of each distribution", "the registry key WSL keeps for each distribution of this Windows user "
             "(Lxss): its name, flavor, OS version, Store package, folder and disk; Microsoft documents no page for it",
             covered="read for the installs table without starting anything; Rename changes a name in it"),
        Area("Windows files from Linux", "Windows' drives under /mnt (DrvFs), and Linux files from Windows",
             LEARN + "filesystems", covered="Windows paths handed to the Docker instance as /mnt/<drive>/..."),
        Area("Disks", "each distribution's virtual disk, its size and space, physical disks mounted into WSL",
             LEARN + "disk-space", covered="each install's disk and its size shown in the installs table"),
        Area("Networking", "NAT and mirrored modes, localhost forwarding, DNS", LEARN + "networking"),
        Area("WSL 1 and WSL 2", "the two architectures and moving a distribution between them", LEARN + "compare-versions",
             covered="new distributions get WSL 2 (the setup's version step)"),
        Area("Linux GUI apps (WSLg)", "Linux graphical apps in Windows' own windows", LEARN + "tutorials/gui-apps"),
        Area("WSL containers", "containers run by WSL itself (wslc.exe), set up apart from .wslconfig",
             LEARN + "wsl-container-settings"),
        Area("Custom distributions", "a distribution packaged for others to install", LEARN + "build-custom-distro"),
    ),
    calls=(
        Call("wsl --status", "WSL's default distribution and version", "WSL itself",
             used="whether WSL is here: the status, the check, the setup", docs=LEARN + "basic-commands#check-wsl-status"),
        Call("wsl --version", "the versions of WSL and of its Linux kernel", "WSL itself",
             used="the check: WSL 2.4.4 or later and its kernel", docs=LEARN + "basic-commands#check-wsl-version"),
        Call("wsl --install --no-distribution", "WSL itself, no distribution yet", "WSL itself",
             used="the setup's wsl step (Windows asks; a restart may follow)", docs=LEARN + "basic-commands#install",
             writes=True),
        Call("wsl --update", "WSL brought to its newest release", "WSL itself", used="the setup's update step",
             docs=LEARN + "basic-commands#update-wsl", writes=True),
        Call("wsl --set-default-version 2", "the WSL version new distributions get", "WSL 1 and WSL 2",
             used="the setup's version step", docs=LEARN + "basic-commands#set-default-wsl-version", writes=True),
        Call("wsl --list --online", "the distributions wsl --install can fetch", "Distributions from Microsoft's list",
             used="the check, and the newest FedoraLinux-NN on Microsoft's list (kept a minute)",
             docs=LEARN + "basic-commands#list-available-linux-distributions"),
        Call("wsl --install <distribution> --name <name> --location <folder> --no-launch",
             "a distribution from Microsoft's list, under a name and in a folder of its own, not launched",
             "Distributions from Microsoft's list", used="the setup's distribution step: Liminal-Fedora from the newest FedoraLinux-NN",
             docs=LEARN + "basic-commands#install", writes=True),
        Call("wsl --list --verbose", "each distribution installed, its state and WSL version", "Installed distributions",
             used="Liminal-Fedora's state, and the installs table", docs=LEARN + "basic-commands#list-installed-linux-distributions"),
        Call("wsl -d <distribution> -u root --exec sh -s", "a shell script run as root, given on standard input",
             "Running commands inside",
             used="the setup's scripts (the default user, Docker's install, the engine, the docker group), Update packages, the services scan",
             docs=LEARN + "basic-commands#run-a-specific-linux-distribution-from-powershell-or-cmd", writes=True),
        Call("wsl -d <distribution> -u root --exec sh -c", "a shell command run as root",
             "Running commands inside", used="/etc/wsl.conf written; Pause and the resume after it (systemd's freezer)",
             docs=LEARN + "basic-commands#run-as-a-specific-user", writes=True),
        Call("wsl -d <distribution> --exec docker", "Docker's command line inside, as the default user",
             "Running commands inside",
             used="Docker's version and whether its daemon answers; the Docker instance wsl-fedora offered to the framework"),
        Call("wsl -d <distribution> --exec <command>", "any command inside, as the default user", "Running commands inside",
             used="the run hook: a command the platform asks for"),
        Call(KEEP_RUNNING, "a windowless session holding a distribution up", "Running commands inside",
             used="Start: the install keeps running until Stop"),
        Call("wsl -d <distribution> --cd ~ --exec sh -c <login shell>", "a login shell in the home folder",
             "Running commands inside", used="Terminal: a login shell in the platform's terminal panel",
             docs=LEARN + "basic-commands#start-wsl-in-user-home-directory"),
        Call("wsl --terminate <distribution>", "a distribution stopped: every program in it ends", "Stopping and removing",
             used="Stop; the restart after /etc/wsl.conf is written; before a rename", docs=LEARN + "basic-commands#terminate",
             writes=True),
        Call("wsl --unregister <distribution>", "a distribution removed with its disk, for good", "Stopping and removing",
             used="Uninstall (one of yours only after a second confirmation)",
             docs=LEARN + "basic-commands#unregister-or-uninstall-a-linux-distribution", writes=True),
        Call(r"HKCU\Software\Microsoft\Windows\CurrentVersion\Lxss (read)", "WSL's record of each distribution",
             "WSL's record of each distribution", used="each install's flavor, OS version, Store package, folder and disk"),
        Call(r"Lxss\{GUID} DistributionName (set)", "a distribution's name in WSL's record", "WSL's record of each distribution",
             used="Rename: WSL has no command for it (the install is stopped first)", writes=True),
        Call("wsl --shutdown", "every distribution and WSL's virtual machine stopped", "Stopping and removing",
             docs=LEARN + "basic-commands#shutdown", writes=True),
        Call("wsl --set-default <distribution>", "the distribution plain wsl commands use", "Installed distributions",
             docs=LEARN + "basic-commands#set-default-linux-distribution", writes=True),
        Call("wsl --set-version <distribution> <1|2>", "a distribution moved between WSL 1 and WSL 2", "WSL 1 and WSL 2",
             docs=LEARN + "basic-commands#set-wsl-version-to-1-or-2", writes=True),
        Call("wsl --import <distribution> <folder> <file>", "a distribution from a tar file (or a .vhdx with --vhd)",
             "Importing and exporting", docs=LEARN + "basic-commands#import-a-distribution", writes=True),
        Call("wsl --export <distribution> <file>", "a distribution saved as a tar file (or a .vhdx with --vhd)",
             "Importing and exporting", docs=LEARN + "basic-commands#export-a-distribution"),
        Call("wsl --mount <disk>", "a physical or virtual disk attached to WSL 2 and mounted", "Disks",
             docs=LEARN + "wsl2-mount-disk", writes=True),
        Call("wsl --list --running", "the distributions running now", "Installed distributions",
             docs=LEARN + "basic-commands#list-installed-linux-distributions"),
        Call("wsl --update --pre-release", "WSL's newest preview", "WSL itself", docs=LEARN + "install", writes=True),
    ),
    verified=VERIFIED,
)

DNF = Api(
    name="DNF (Fedora's packages)",
    maker="the Fedora Project (DNF5)",
    about=("Fedora's package manager: dnf (DNF5 since Fedora 41) reads the repositories' metadata, installs and upgrades "
           "packages with what they depend on, and adds repositories with its config-manager. The plugin runs it as root "
           "inside the install to bring its packages up to date and to install Docker from Docker's own repository."),
    kind="command",
    base="dnf, as root inside the install (through wsl -u root)",
    version="DNF5 (Fedora 41 and later); DNF 4's config-manager --add-repo is tried where addrepo is not known",
    auth=("root inside the install; Fedora's repositories and Docker's are public, their packages checked against the "
          "repositories' GPG keys"),
    limits="",
    costs="",
    links=(
        Link("DNF5's documentation", DNF5, "docs"),
        Link("dnf5-upgrade(8)", DNF5 + "commands/upgrade.8.html", "reference"),
        Link("dnf5-install(8)", DNF5 + "commands/install.8.html", "reference"),
        Link("dnf5-config-manager(8)", DNF5 + "dnf5_plugins/config-manager.8.html", "reference"),
        Link("Using the DNF software package manager (Fedora)", "https://docs.fedoraproject.org/en-US/quick-docs/dnf/", "guide"),
        Link("Fedora in WSL", "https://docs.fedoraproject.org/en-US/cloud/wsl/", "guide"),
        Link("Changes from DNF4", DNF5 + "changes_from_dnf4.7.html", "changelog"),
        Link("DNF5 releases", "https://github.com/rpm-software-management/dnf5/releases", "changelog"),
        Link("DNF5's source", "https://github.com/rpm-software-management/dnf5", "source"),
        Link("Fedora's infrastructure status", "https://status.fedoraproject.org/", "status"),
    ),
    areas=(
        Area("Upgrading", "the installed packages brought to the repositories' newest", DNF5 + "commands/upgrade.8.html",
             covered="Update packages: every package upgraded, the metadata refreshed first"),
        Area("Installing", "packages and their dependencies", DNF5 + "commands/install.8.html",
             covered="DNF 4's plugins (dnf-plugins-core), then Docker's packages"),
        Area("Repositories", "the repositories dnf reads, added from a .repo file", DNF5 + "dnf5_plugins/config-manager.8.html",
             covered="Docker's docker-ce.repo added (DNF5's addrepo, else DNF 4's --add-repo)"),
        Area("Repository information", "the repositories configured and their state", DNF5 + "commands/repo.8.html"),
        Area("Removing", "packages removed with what only they needed", DNF5 + "commands/remove.8.html"),
        Area("Searching", "packages found by name and summary", DNF5 + "commands/search.8.html"),
        Area("Metadata", "the repositories' metadata kept and refreshed", DNF5 + "commands/makecache.8.html"),
        Area("Configuration", "dnf5.conf: what dnf does by default", DNF5 + "dnf5.conf.5.html"),
        Area("DNF4 to DNF5", "what changed in commands and options", DNF5 + "changes_from_dnf4.7.html",
             covered="both forms of adding a repository are tried"),
        Area("Fedora in WSL", "Fedora's own pages on its WSL images", "https://docs.fedoraproject.org/en-US/cloud/wsl/",
             covered="the newest FedoraLinux-NN on Microsoft's list is the one installed"),
    ),
    calls=(
        Call("dnf -y upgrade --refresh", "every package upgraded, the metadata read again first", "Upgrading",
             used="Update packages", docs=DNF5 + "commands/upgrade.8.html", writes=True),
        Call("dnf -y install dnf-plugins-core", "DNF 4's plugins, config-manager among them", "Installing",
             used="before Docker's repository is added", docs=DNF5 + "commands/install.8.html", writes=True),
        Call("dnf -y config-manager addrepo --from-repofile=<url>", "a repository added from its .repo file (DNF5)",
             "Repositories", used="Docker's repository", docs=DNF5 + "dnf5_plugins/config-manager.8.html", writes=True),
        Call("dnf -y config-manager --add-repo <url>", "a repository added (DNF 4)", "Repositories",
             used="Docker's repository, where addrepo is not known", writes=True),
        Call("dnf -y install <packages>", "packages installed with their dependencies", "Installing",
             used="Docker's packages", docs=DNF5 + "commands/install.8.html", writes=True),
        Call("dnf repo list", "the repositories configured", "Repository information", docs=DNF5 + "commands/repo.8.html"),
        Call("dnf remove <packages>", "packages removed", "Removing", docs=DNF5 + "commands/remove.8.html", writes=True),
        Call("dnf search <words>", "packages found by their name and summary", "Searching", docs=DNF5 + "commands/search.8.html"),
        Call("dnf makecache", "the repositories' metadata read and kept", "Metadata", docs=DNF5 + "commands/makecache.8.html"),
    ),
    verified=VERIFIED,
)

DOCKER_ENGINE = Api(
    name="Docker Engine",
    maker="Docker, Inc.",
    about=("Docker's container engine for Linux: the dockerd daemon and the docker command line, with containerd beneath "
           "them and the Buildx and Compose plugins, installed from Docker's own rpm repository for Fedora. The plugin "
           "installs and starts it inside Liminal-Fedora and offers it to the framework as the Docker instance wsl-fedora, "
           "reached as `wsl -d Liminal-Fedora --exec docker`."),
    kind="command",
    base="docker inside Liminal-Fedora, from https://download.docker.com/linux/fedora",
    version="Docker Engine's stable channel for Fedora (Fedora 43 to 45 are the releases its page supports)",
    auth=("the docker group: its members (the install's default user) reach the daemon without sudo, which is root's "
          "power over the install"),
    limits="",
    costs="",
    links=(
        Link("Install Docker Engine on Fedora", DOCKER + "engine/install/fedora/", "docs"),
        Link("Linux post-installation steps", DOCKER + "engine/install/linux-postinstall/", "guide"),
        Link("Docker CLI reference", DOCKER + "reference/cli/docker/", "reference"),
        Link("dockerd reference", DOCKER + "reference/cli/dockerd/", "reference"),
        Link("Docker Engine release notes", DOCKER + "engine/release-notes/", "changelog"),
        Link("Docker's rpm repository for Fedora", "https://download.docker.com/linux/fedora/", "source"),
        Link("Docker's status", "https://www.dockerstatus.com/", "status"),
    ),
    areas=(
        Area("The rpm repository", "Docker's repository, added to dnf from its docker-ce.repo",
             DOCKER + "engine/install/fedora/#set-up-the-repository", covered="added by dnf's config-manager"),
        Area("The packages", "docker-ce, docker-ce-cli, containerd.io, docker-buildx-plugin, docker-compose-plugin",
             DOCKER + "engine/install/fedora/#install-docker-engine", covered="installed by dnf from the repository"),
        Area("The daemon", "dockerd, started by the init and on at boot", DOCKER + "reference/cli/dockerd/",
             covered="started and enabled at boot: systemd, else OpenRC, else the service command"),
        Area("Docker without sudo", "the docker group, whose members reach the daemon",
             DOCKER + "engine/install/linux-postinstall/#manage-docker-as-a-non-root-user",
             covered="the install's default user put in the docker group"),
        Area("The command line", "docker's commands: containers, images, volumes, networks, the system",
             DOCKER + "reference/cli/docker/",
             covered="docker --version and docker info say whether it is installed and running; the Docker plugin drives the rest"),
        Area("Upgrades", "Docker's packages upgraded with the system's", DOCKER + "engine/install/fedora/",
             covered="with the install's packages (Update packages)"),
        Area("Rootless mode", "the daemon run as an ordinary user", DOCKER + "engine/security/rootless/"),
        Area("Uninstalling", "Docker's packages removed, its images and volumes deleted",
             DOCKER + "engine/install/fedora/#uninstall-docker-engine"),
    ),
    calls=(
        Call("GET https://download.docker.com/linux/fedora/docker-ce.repo", "Docker's repository file", "The rpm repository",
             used="added by dnf's config-manager", docs=DOCKER + "engine/install/fedora/#set-up-the-repository"),
        Call("dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
             "Docker Engine's packages", "The packages", used="the setup's docker step",
             docs=DOCKER + "engine/install/fedora/#install-docker-engine", writes=True),
        Call("systemctl enable --now docker", "the daemon started and on at boot (systemd)", "The daemon",
             used="the setup's engine step", docs=DOCKER + "engine/install/fedora/#install-docker-engine", writes=True),
        Call("rc-service docker start", "the daemon started (OpenRC, after rc-update add docker default)", "The daemon",
             used="the engine step, when the install runs OpenRC", writes=True),
        Call("service docker start", "the daemon started by its init script", "The daemon",
             used="the engine step, when the install runs neither systemd nor OpenRC", writes=True),
        Call("groupadd -f docker", "the docker group, made when absent", "Docker without sudo", used="the setup's user step",
             docs=DOCKER + "engine/install/linux-postinstall/#manage-docker-as-a-non-root-user", writes=True),
        Call("usermod -aG docker <user>", "a user added to the docker group", "Docker without sudo",
             used="the setup's user step", docs=DOCKER + "engine/install/linux-postinstall/#manage-docker-as-a-non-root-user",
             writes=True),
        Call("docker --version", "the command line's version", "The command line", used="whether Docker is installed",
             docs=DOCKER + "reference/cli/docker/version/"),
        Call("docker info --format {{.ServerVersion}}", "the daemon's version, when it answers", "The command line",
             used="whether the daemon runs", docs=DOCKER + "reference/cli/docker/system/info/"),
        Call("docker run hello-world", "a first container, the install's check", "The command line",
             docs=DOCKER + "engine/install/fedora/#install-docker-engine"),
        Call("dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
             "Docker's packages removed", "Uninstalling", docs=DOCKER + "engine/install/fedora/#uninstall-docker-engine",
             writes=True),
    ),
    verified=VERIFIED,
)

INIT = Api(
    name="systemd (the install's init)",
    maker="the systemd project",
    about=("systemd, the init and service manager the install runs as PID 1 once /etc/wsl.conf turns it on: it starts "
           "the services, lists them with their state and memory, and can freeze a service's processes and thaw them. The "
           "plugin's services scan reads it (or OpenRC's or SysV's, when an install runs those), and its Pause and the "
           "resume after it are systemd's freezer."),
    kind="command",
    base="systemctl, as root inside the install (through wsl -u root)",
    version="systemd 246 or later for the freezer (cgroup v2, which WSL mounts by default)",
    auth="root inside the install",
    limits="",
    costs="",
    links=(
        Link("systemctl(1)", SYSTEMD + "systemctl.html", "reference"),
        Link("systemd's manual pages", SYSTEMD, "docs"),
        Link("Use systemd to manage Linux services with WSL", LEARN + "systemd", "guide"),
        Link("systemd's news", "https://github.com/systemd/systemd/blob/main/NEWS", "changelog"),
        Link("systemd's source", "https://github.com/systemd/systemd", "source"),
    ),
    areas=(
        Area("Units and their state", "every service unit, loaded or not, active or failed", SYSTEMD + "systemctl.html",
             covered="the services scan: each service's state, the running ones' memory"),
        Area("Freezing", "a unit's processes suspended in their cgroup, and thawed", SYSTEMD + "systemctl.html",
             covered="Pause freezes each running service but the system's own plumbing; Start thaws them"),
        Area("Starting and stopping", "units started, stopped, restarted, enabled at boot", SYSTEMD + "systemctl.html",
             covered="Docker's daemon enabled and started (the Docker Engine card)"),
        Area("The journal", "the services' logs", SYSTEMD + "journalctl.html"),
        Area("Unit files", "how a service is described: what it runs, when, as whom", SYSTEMD + "systemd.unit.html"),
        Area("Other inits", "OpenRC (rc-status) and SysV scripts (service), for an install that runs those",
             "https://github.com/OpenRC/openrc/blob/master/man/rc-status.8",
             covered="the services scan reads them the same way when the install's init is one of them"),
        Area("Processes", "every process with its memory, as ps lists them", "https://man7.org/linux/man-pages/man1/ps.1.html",
             covered="the services scan counts them beside the units"),
    ),
    calls=(
        Call("systemctl list-units --type=service", "the service units and their states", "Units and their state",
             used="the services scan; Pause's list of the running services", docs=SYSTEMD + "systemctl.html"),
        Call("systemctl show -p Id -p MainPID -p MemoryCurrent <units>", "properties of the running services",
             "Units and their state", used="the services scan: each running service's process and memory",
             docs=SYSTEMD + "systemctl.html"),
        Call("systemctl freeze <unit>", "a unit's processes frozen", "Freezing", used="Pause", docs=SYSTEMD + "systemctl.html",
             writes=True),
        Call("systemctl thaw <unit>", "a frozen unit's processes thawed", "Freezing", used="Start after Pause",
             docs=SYSTEMD + "systemctl.html", writes=True),
        Call("systemctl show -p Id -p FreezerState --type=service '*'", "which services are frozen", "Freezing",
             used="the resume: any service still frozen is thawed too", docs=SYSTEMD + "systemctl.html"),
        Call("rc-status --all", "OpenRC's services and their states", "Other inits",
             used="the services scan, when the install runs OpenRC", docs="https://github.com/OpenRC/openrc/blob/master/man/rc-status.8"),
        Call("service --status-all", "the SysV scripts' states", "Other inits",
             used="the services scan, when the install runs neither"),
        Call("ps -eo pid=,rss=,comm=,args=", "every process, its memory and command", "Processes",
             used="the services scan: the processes and their memory", docs="https://man7.org/linux/man-pages/man1/ps.1.html"),
        Call("systemctl restart <unit>", "a unit stopped and started", "Starting and stopping", docs=SYSTEMD + "systemctl.html",
             writes=True),
        Call("journalctl -u <unit>", "a unit's log", "The journal", docs=SYSTEMD + "journalctl.html"),
    ),
    verified=VERIFIED,
)

APIS = (WSL, DNF, DOCKER_ENGINE, INIT)


def ago(when: float, now: float | None = None) -> str:
    """A time on the monotonic clock, said as how long ago: "40 s ago", "3 min ago", "2 h ago"."""
    s = max(0.0, (time.monotonic() if now is None else now) - when)
    return f"{s:.0f} s ago" if s < 90 else f"{s / 60:.0f} min ago" if s < 5400 else f"{s / 3600:.0f} h ago"


def count(n: int, word: str) -> str:
    return f"{n} {word}" + ("" if n == 1 else "s")


def facts(plugin) -> dict[str, dict[str, str]]:
    """What the plugin kept of its APIs while it ran (asking nothing): Microsoft's list as last read (its newest Fedora),
    Docker inside as last seen, the init the last services scan found."""
    out: dict[str, dict[str, str]] = {}
    online = getattr(getattr(plugin, "wsl", None), "_online", None)  # (when, names): wsl --list --online, kept a minute
    if online:
        at, names = online
        fedoras = sorted((n for n in names if n.lower().startswith("fedoralinux-")), reverse=True)
        out[WSL.name] = {"Microsoft's list": f"{len(names)} distributions, read {ago(at)}",
                         "Newest Fedora on it": fedoras[0] if fedoras else "none"}
    seen = getattr(plugin, "_engine_seen", None)  # docker --version and docker info, as last seen while it ran
    if seen:
        out[DOCKER_ENGINE.name] = {"Docker inside": (f"{seen.get('version') or 'installed'}, its daemon "
                                                     + ("answering" if seen.get("running") else "not answering")
                                                     if seen.get("installed") else "not installed") + " (as last seen)"}
    kept = getattr(plugin, "_scan", None)  # (when, Scan): the last services scan
    if kept:
        at, scan = kept
        words = scan.problem or f"{count(len(scan.major), 'service')} of note, {len(scan.system)} of the system's own running"
        out[INIT.name] = {"Init": scan.init + (f" (PID 1: {scan.pid1})" if scan.pid1 else ""),
                          "Last scan": f"{words}, {ago(at)}"}
    return out
