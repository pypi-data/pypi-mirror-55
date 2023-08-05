import sysdef.emulator
import logging

logger = logging.getLogger(__name__)


"""
examples
```
pip3:
    packages:
        - "mycoolpkg"
        - "somethingelse --pre"
        - "something=1.2.3
```
"""

def get_cmd(package):
    return f"pip3 install {package}"


def process_2_needed(data):
    return data.get("packages", [])


def process_1(data, g=None):
    pass


def process_2(data, ssh_session):
    """
    After much deliberation and indecision, the best way I can think of to
    install python libraries is the good old pip command run under the
    emulator as part of stage 2.

    Alternatives:
    *   (for sysdef package only) - find the currently executing file, work
        out parent dir, tar up and tar-in to disk image using guestfs.
        should mostly work but pip-generated shims such as the main `sysdef`
        command would be missing and need ugly workarounds to recreate
    *   As-above but download and unpack wheels from pypi instead of finding
        the currently executing file. This allows installing other libraries
        but has the same disadvantages and is more complicated

    Gotchas:
    *   No support for python packages that need to compile C code since our
        base OS doesn't ship with a C compiler. Suggest adding such libraries
        to the base OS image instead - see
        http://buildroot.uclibc.org/downloads/manual/manual.html#adding-packages
    """

    # contain all packages to install inside `packages` so that we can go back
    # and add `settings` etc in the future if needed
    for package in process_2_needed(data):
        logger.info("pip3 installing %s", package)
        sysdef.emulator.command(get_cmd(package), ssh_session)


def process(data, root=""):
    for package in process_2_needed(data):
        logger.info("pip3 installing %s", package)
        sysdef.util.run(get_cmd(package))
