"""WSL Fedora for Liminal (the user, 2026-11-07: "the platform is the interface for the software/hardware
which facilitates the liminal framework"; "the scope of the plugin is setting up WSL/Ubuntu and supporting
docker for the platform"; "then create a gentoo and fedora plugin as well, same scope/function"): Fedora
in WSL 2 on this Windows PC, set up by the plugin (WSL itself, the distribution, systemd and the default
user, Docker inside, the engine started, the user in the docker group), and its engine offered to the
framework as the Docker instance `wsl-fedora` (liminal_libs.docker.instances). Everything is the library's
WslDistribution (liminal_libs.machines.wsl); this module says which distribution.

    python -m plugin_platform_wsl_fedora status | setup [STEP ...] | run -- COMMAND | instances
"""
from __future__ import annotations

import os

from liminal_libs.machines.wsl import WslDistribution, WslError

__version__ = "0.1.1"


def _read_text(url: str) -> str:
    import urllib.request

    with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 - the plugin's own url
        return r.read().decode("utf-8", "replace")


class WslFedoraPlugin(WslDistribution):
    name = "wsl-fedora"
    title = "WSL Fedora"
    about = "Fedora in WSL 2 on this Windows PC, with Docker inside: the Linux the platform's containers run in"
    api = "2.1"
    order = 701
    distribution = "FedoraLinux-42"
    family = "dnf"
    docker_repository = "https://download.docker.com/linux/fedora"  # Docker's own, as its documentation gives it
    install_name = "FedoraLinux-42"
    DISTRIBUTION_VAR = "WSL_FEDORA_DISTRIBUTION"
    USER_VAR = "WSL_FEDORA_USER"

    @property
    def distribution_name(self) -> str:
        """WSL_FEDORA_DISTRIBUTION, else the Fedora installed (FedoraLinux-NN), else the newest on Microsoft's list,
        else FedoraLinux-42 (the name carries the release)."""
        named = (os.environ.get(self.DISTRIBUTION_VAR) or "").strip()
        if named:
            return named
        try:
            installed = sorted((d.name for d in self.wsl.distributions() if d.name.lower().startswith("fedora")), reverse=True)
            if installed:
                return installed[0]
            online = sorted((n for n in self.wsl.online() if n.lower().startswith("fedoralinux-")), reverse=True)
            if online:
                return online[0]
        except Exception:  # noqa: BLE001 - no WSL to ask: the default name
            pass
        return self.distribution

    @property
    def install_name(self) -> str:  # type: ignore[override]
        return self.distribution_name


MACHINE = WslFedoraPlugin()
