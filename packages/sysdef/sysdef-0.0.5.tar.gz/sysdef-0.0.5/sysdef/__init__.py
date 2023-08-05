#!/usr/bin/env python3
import sys
import shutil
import logging
import argparse
import sysdef.util
import traceback
import importlib
import sysdef.disk_image
import sysdef.interpreter.overlay
import sysdef.emulator
import sysdef.interpreter.meta
import pkg_resources  # part of setuptools
import sysdef.interpreter.meta
import sysdef.interpreter.meta

sysdef_yaml = {}
logger = logging.getLogger(__name__)


def setup_logging(level, logger_name=__name__):
    _logger = logging.getLogger(logger_name)
    _logger.setLevel(level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s"))
    _logger.addHandler(console_handler)

    _logger.debug("====[debug mode enabled]====")

def lookup(stage, section=None):
    data = sysdef_yaml.get(stage, {})
    if section:
        data = data.get(section, {})
    return data


def sysdef_image(image_file, sysdef_file):
    s = sysdef.util.parse(sysdef_file, "image")

    _image_file = copy_image(image_file)

    # make a temporary overlay disk image
    overlay_data = s.get("overlay", False)
    g, temp_overlay_image = sysdef.disk_image.init(overlay_data, _image_file)

    #
    # Image stage 1 - libguestfs access to files inside image
    #
    interpreter_modules = {}
    logger.info("starting image stage 1...")
    for sect in s:
        logger.info(f"processing section: {sect}")
        # https://stackoverflow.com/questions/10675054/how-to-import-a-module-in-python-with-importlib-import-module
        interpreter_module = importlib.import_module("." + sect, package="sysdef.interpreter")

        # if we have a `process_1()` function then this takes precedence over `process()`
        f = getattr(interpreter_module, "process_1", False) or getattr(interpreter_module, "process")
        result = f(s.get(sect), g=g)
        interpreter_modules[sect] = interpreter_module

    logger.info("stage 1 complete - shutting down libguestfs")
    g.shutdown()

    #
    # Image stage 2 - boot image file(s) inside emulator
    #
    stage_2_required = sysdef.interpreter.meta.stage2_required(interpreter_modules, s)
    if stage_2_required:
        logger.info("starting stage 2 - booting emulator")
        session = sysdef.emulator.start_emulator_and_get_ssh_session(
            _image_file,
            temp_overlay_image
        )
        for sect in stage_2_required:
            logger.info(f"processing section: {sect}")
            interpreter_module = stage_2_required[sect]

            # we are guaranteed a `process_2` function due to earlier dict filtering
            f = getattr(interpreter_module, "process_2")
            result = f(s.get(sect), session)

        logger.info("Done!... shutting down emulator")
        sysdef.emulator.stop_emulator(session)

    logger.info("system built, preparing disk image...")
    if temp_overlay_image:
        sysdef.disk_image.absorb(_image_file, temp_overlay_image)

    sysdef.disk_image.convert_to_hybrid(_image_file)
    logger.info("...done!")


def sysdef_boot(sysdef_file, root=""):
    s = sysdef.util.parse(sysdef_file, "boot")
    try:
        for sect in s:
            logger.info(f"processing section: {sect}")
            # https://stackoverflow.com/questions/10675054/how-to-import-a-module-in-python-with-importlib-import-module
            interpreter_module = importlib.import_module("." + sect, package="sysdef.interpreter")

            # if we have a `process_1()` function then this takes precedence over `process()`
            f = getattr(interpreter_module, "process")
            result = f(s.get(sect), root=root)
    except ModuleNotFoundError as e:
        logger.error(f"Missing interpreter for section: {e.name}")


def copy_image(image_file):
    working_copy = image_file + "-working"
    shutil.copy(image_file, working_copy)
    return working_copy


def interactive(image_file):
    logger.info("starting emulator")
    sysdef.emulator.start_emulator_interactive(copy_image(image_file))


def version():
    return pkg_resources.require("sysdef")[0].version



def main():
    parser = argparse.ArgumentParser(description="""
    sysdef configuration management system
    """)

    parser.add_argument('--image-file',
                        help='select image mode and write this file')
    parser.add_argument('--sysdef-file',
                        default=sysdef.interpreter.meta.config_file,
                        help='read input from this file')
    parser.add_argument('--boot',
                        default=False,
                        action='store_true',
                        help='apply sysdef to this machine')
    parser.add_argument('--debug',
                        default=False,
                        action='store_true',
                        help='debug mode enabled')
    parser.add_argument('--interactive',
                        default=False,
                        action='store_true',
                        help='Boot the SD card for interactive shell')
    parser.add_argument('--version',
                        default=False,
                        action='store_true',
                        help='Print the sysdef version and exit')
    args = parser.parse_args()
    setup_logging(
        logging.DEBUG if args.debug else logging.INFO
    )

    try:
        if args.image_file and args.interactive:
            interactive(args.image_file)
        elif args.image_file:
            sysdef_image(args.image_file, args.sysdef_file)
        elif args.boot:
            sysdef_boot(args.sysdef_file)
        elif args.version:
            print(version())
        else:
            print("Must specify one of --image-file or --boot")
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(str(exc_value))
        if args.debug:
            traceback.print_exception(exc_type, exc_value, exc_traceback)

