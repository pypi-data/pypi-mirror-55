import sysdef
import importlib
import logging
import os
import pkg_resources
import sysdef.util

logger = logging.getLogger(__name__)

config_file = "/etc/sysdef/sysdef.yaml"


def install_needed(data):
    return data.get("install", True)


def install_systemd(g=None, root=""):
    unit_file = "/usr/lib/systemd/system/sysdef.service"
    activation_link = "/etc/systemd/system/multi-user.target.wants/sysdef.service"
    changes = False
    sysdef_service_content = pkg_resources.resource_string(__name__, "../res/sysdef.service")

    changes |= sysdef.util.mkfile(unit_file, content=sysdef_service_content, g=g, root=root)
    changes |= sysdef.util.ln_s(unit_file, activation_link, g=g, root=root)

    if not g and not root and changes:
        logger.info("systemd scripts installed, rebooting to take effect")
        sysdef.util.reboot()


def stage2_required(interpreter_modules, data):
    """
    Filter the list of interpreters to use so that only those that need to take
    action in image stage 2 (emulator) are left. This results in a dict with
    zero or more members
    """
    return {k: v for (k, v) in interpreter_modules.items() if getattr(v, "process_2", False) and v.process_2_needed(data.get(k, {}))}


def process_1(data, g=None):
    if install_needed(data):
        logger.info(f"installing config file for sysdef at {config_file}")
        config_data = {
            "sysdef": {
                "boot": sysdef.lookup("boot")
            }
        }
        sysdef.util.mkdir(os.path.dirname(config_file), g=g)
        sysdef.util.save_yaml(config_file, config_data, g=g)

        install_systemd(g=g)


def process_2(data, ssh_session):
    if install_needed(data):
        inline_sysdef = {
            "packages": [f"sysdef=={sysdef.version()}"]
        }

        logger.info("installing sysdef")
        provider_mod = importlib.import_module(".pip3", package="sysdef.interpreter")
        provider_mod.process_2(inline_sysdef, ssh_session)


def process_2_needed(data):
    return data.get("install", True)

def process(data, root="", g=None):
    if install_needed(data):
        install_systemd(g=g, root=root)
