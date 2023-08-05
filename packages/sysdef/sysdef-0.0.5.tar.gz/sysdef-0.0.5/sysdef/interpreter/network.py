import logging
import sysdef.util

logger = logging.getLogger(__name__)

DEFAULT_HOSTNAME = "sysdef"


def read_etc_hostname(root="", g=None):
    etc_hostname_file = root + "/etc/hostname"
    etc_hostname_data = sysdef.util.readlines(etc_hostname_file, g)

    return etc_hostname_data[0].strip()


def process(data, root="", g=None):
    etc_hostname = root + "/etc/hostname"
    hostname = data.get("hostname", DEFAULT_HOSTNAME)
    image_hostname = read_etc_hostname(g=g)

    if hostname != image_hostname:
        logger.info("setting hostname: %s", hostname)
        sysdef.util.savelines([hostname], etc_hostname, g=g)

    if g is None:
        # outside of image/real system
        sysdef.util.reboot()
