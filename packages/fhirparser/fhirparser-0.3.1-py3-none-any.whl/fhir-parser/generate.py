import os
from argparse import ArgumentParser, ArgumentError
from types import ModuleType
from typing import List, Optional

import sys

import fhirloader
import fhirspec
from logger import logger

_cache = 'downloads'

def genargs() -> ArgumentParser:
    """
    Create a command line parser

    :return: parser
    """
    parser = ArgumentParser(prog="fhirparser")
    parser.add_argument("settings", help="Location of the settings file. Default is settings.py",
                        default="settings.py")
    parser.add_argument("-f", "--force", help="Force download of the spec", action="store_true")
    parser.add_argument("-c", "--cached", help='Force use of the cached spec (incompatible with "-f")',
                        action="store_true")
    parser.add_argument("-lo", "--loadonly", help="Load the spec but do not parse or write resources",
                        action="store_true")
    parser.add_argument("-po", "--parseonly", help="Load and parse but do not write resources", action="store_true")
    parser.add_argument("-u", "--fhirurl", help="FHIR Specification URL (overrides settings.specifications_url)")
    parser.add_argument("-td", "--templatedir", help="Templates base directory (overrides settings.tpl_base)")
    parser.add_argument("-o", "--outputdir",
                        help = "Directory for generated class models. (overrides settings.tpl_resource_target)")
    parser.add_argument("-cd", "--cachedir", help = f"Cache directory (default: {_cache})", default=_cache)
    return parser


def generator(args: List[str]) -> Optional[int]:
    opts = genargs().parse_args(args)
    if opts.force and opts.cached:
        raise ArgumentError('force and cached options cannot both be true')
    if os.path.isdir(opts.settings):
        opts.settings = os.path.join(os.path.settings, 'settings.py')
    opts.settings_dir = os.path.abspath(os.path.dirname(os.path.settings))
    logger.info(f"Loading settings from {opts.settings}")
    with open(opts.settings) as f:
        settings_py = f.read()
    settings = ModuleType('settings')
    exec(settings_py, settings.__dict__)
    if opts.fhirurl:
        settings.specification_url = opts.fhirurl
    logger.info(f"Specification: {settings.specification_url}")
    if opts.templatedir:
        settings.tpl_base = opts.templatedir
    else:
        settings.tpl_base = os.path.relpath(settings.tpl_base, opts.settings_dir)
    logger.info(f"Template directory: {settings.tpl_base}")
    if opts.outputdir:
        settings.tpl_resource_target = opts.outputdir
    else:
        settings.tpl_resource_target = os.path.relpath(settings.tpl_resource_target, opts.settings_dir)
    settings.tpl_unittest_target = os.path.relpath(settings.tpl_unittest_target, opts.settings_dir)
    logger.info(f"Output directory: {settings.tpl_resource_target}")
    logger.info(f"Cache directory: {opts.cachedir}")

    loader = fhirloader.FHIRLoader(settings, opts.cachedir)
    spec_source = loader.load(force_download=opts.force, force_cache= opts.cached)
    if not opts.loadonly:
        spec = fhirspec.FHIRSpec(spec_source, settings)
        if not opts.parseonly:
            spec.write()
    return 0


if '__main__' == __name__:
    sys.exit(generator(sys.argv[1:]))
