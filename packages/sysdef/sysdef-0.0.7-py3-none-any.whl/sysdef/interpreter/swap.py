import sysdef.util
import importlib
import logging
import os

logger = logging.getLogger(__name__)


def fstab(file, g=None, root=""):
    logger.debug("adding swapfile to /etc/fstab")
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

    logger.info("creating swap file")
    sysdef.emulator.command(dd_comand(data), ssh_session)
    sysdef.emulator.command(mkswap_command(data), ssh_session)

    # Now file is made, in fstab and will be used on reboot - done


def process(data, root=""):
    file = data.get("file", "/swap.dat")
    size = data.get("size", 512)
    if data.get("enabled", True):
        changes = False
        if os.path.isfile(file) and os.stat(file).st_size != size * 1024**2:
            logger.info(f"swapfile exists at {file} but is wrong size - deleting")
            sysdef.util.run(f"swapoff {file} ; true")
            os.unlink(file)

        if not os.path.isfile(file):
            logger.info("Creating swap file...")
            sysdef.util.run(dd_comand(data, root=root))
            sysdef.util.run(mkswap_command(data, root=root))
            changes = True

        # any fstab changes will reboot system
        fstab(file, root=root)

        if changes:
            # if we had to recreate swap file (eg size) then just activate it
            # if we haven't already rebooted
            logger.info("activating swap...")
            sysdef.util.run("swapon -a")



