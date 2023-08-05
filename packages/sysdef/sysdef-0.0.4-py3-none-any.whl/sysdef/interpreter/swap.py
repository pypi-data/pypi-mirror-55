import sysdef.util
import importlib


def fstab(file, g=None, root=""):

    inline_sysdef = {
        file: {
            "mount_point": "none",
            "type": "swap",
            "options": "default",
            "dump": 0,
            "pass": 0,
        }
    }
    provider_mod = importlib.import_module(".mounts", package="sysdef.interpreter")
    provider_mod.process(inline_sysdef, g=g, root=root)


def process_1(data, g=None):
    file = data.get("file")
    fstab(file, g=g)


def process_2_needed(data):
    return data.get("file", False)


def dd_comand(data, root=""):
    size = data.get("size")
    file = data.get("file")
    _file = root + file
    return f"dd if=/dev/zero of={_file} bs={1024**2} count={size}"


def mkswap_command(data, root=""):
    file = data.get("file")
    _file = root + file
    return f"mkswap {_file}"


def process_2(data, ssh_session):
    size = data.get("size")
    file = data.get("file")

    sysdef.emulator.command(dd_comand(data), ssh_session)
    sysdef.emulator.command(mkswap_command(data), ssh_session)

    # Now file is made, in fstab and will be used on reboot - done


def process(data, root=""):
    file = data.get("file")

    sysdef.util.run(dd_comand(data, root=root))
    sysdef.util.run(mkswap_command(data, root=root))

    fstab(file, root=root)

    sysdef.util.run("swapon -a")


