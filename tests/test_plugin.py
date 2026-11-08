"""WSL Fedora: the distribution it names, its family, its variables, its engine as a Docker instance, all
through a stand-in wsl command (nothing runs here)."""
from __future__ import annotations

import pytest

from liminal_libs.machines.wsl import Wsl, WslError  # noqa: F401
from plugin_platform_wsl_fedora import MACHINE, WslFedoraPlugin


def u16(text):
    return text.encode("utf-16-le")


class FakeWsl:
    def __init__(self, distributions=(), online=("Ubuntu", "FedoraLinux-42"), docker=False):
        self.distributions = list(distributions)
        self.online = list(online)
        self.docker = docker
        self.calls = []

    def __call__(self, args, timeout):
        self.calls.append(list(args))
        if args[1] == "--status":
            return 0, u16("Default Distribution: Ubuntu\r\nDefault Version: 2\r\n"), b""
        if args[1:3] == ["--list", "--verbose"]:
            return 0, u16("  NAME STATE VERSION\r\n" + "".join(f"  {n} {s} {v}\r\n" for n, s, v in self.distributions)), b""
        if args[1:3] == ["--list", "--online"]:
            return 0, u16("NAME FRIENDLY\r\n" + "".join(f"{n} x\r\n" for n in self.online)), b""
        if args[1] == "-d":
            command = args[args.index("--exec") + 1:]
            if command[:2] == ["docker", "--version"]:
                return (0, b"Docker version 28.1.1, build x\n", b"") if self.docker else (127, b"", b"not found")
            if command[:2] == ["docker", "info"]:
                return (0, b"28.1.1\n", b"") if self.docker else (1, b"", b"no daemon")
            return 0, (" ".join(command) + "\n").encode(), b""
        return 0, u16("ok"), b""


def test_the_plugin_names_its_distribution_and_offers_its_engine(monkeypatch):
    monkeypatch.delenv("WSL_FEDORA_DISTRIBUTION", raising=False)
    monkeypatch.delenv("WSL_FEDORA_USER", raising=False)
    assert MACHINE.name == "wsl-fedora" and MACHINE.family == "dnf" and MACHINE.SYSTEM == "platform" and MACHINE.KIND == "machine"
    assert MACHINE.options == ("WSL_FEDORA_DISTRIBUTION", "WSL_FEDORA_USER") and MACHINE.user == "liminal"
    fake = FakeWsl(distributions=[("Liminal-Fedora", "Running", "2")], docker=True)
    p = WslFedoraPlugin(wsl=Wsl(runner=fake))
    assert p.present() and p.status()["engine"]["installed"] and p.status()["family"] == "dnf"
    (inst,) = p.instances()
    assert inst.name == "wsl-fedora" and inst.command == f"wsl -d {p.distribution_name} --exec docker" and inst.translate("C:\\\\x") == "/mnt/c/x"
    assert p.run("echo", "hi") == "echo hi\n"
    assert WslFedoraPlugin(wsl=Wsl(runner=FakeWsl())).instances() == ()


def test_liminals_fedora_is_installed_from_the_newest_offered_and_never_the_users(monkeypatch):
    monkeypatch.delenv("WSL_FEDORA_DISTRIBUTION", raising=False)
    fake = FakeWsl(distributions=[("Ubuntu", "Stopped", "2")], online=["Ubuntu", "FedoraLinux-42", "FedoraLinux-43"])
    p = WslFedoraPlugin(wsl=Wsl(runner=fake))
    assert p.distribution_name == "Liminal-Fedora" and p.install_name == "FedoraLinux-43"  # the newest offered
    fake.distributions.append(("FedoraLinux-42", "Running", "2"))  # the user's own Fedora
    assert not p.present() and p.status()["valid"] is False and p.status()["why"] == "no Liminal install: its setup installs Liminal-Fedora"
    fake.distributions.append(("Liminal-Fedora", "Running", "2"))
    assert p.present() and p.status()["valid"] is True
    assert WslFedoraPlugin(wsl=Wsl(runner=FakeWsl(online=[]))).install_name == "FedoraLinux-42"  # the list unread: the fallback
    monkeypatch.setenv("WSL_FEDORA_DISTRIBUTION", "Fedora-custom")
    assert p.distribution_name == "Fedora-custom" and p.status()["valid"] is False  # named as the user's: not Liminal's


def test_docker_comes_from_dockers_own_repository_for_the_distribution():
    script = MACHINE.install_script()
    assert MACHINE.docker_repository == "https://download.docker.com/linux/fedora" and "{repository}" not in script
    assert "--from-repofile=https://download.docker.com/linux/fedora/docker-ce.repo " in script and "dnf -y install docker-ce " in script
