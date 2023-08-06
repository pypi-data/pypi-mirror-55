import os
from argparse import ArgumentParser, ArgumentError
from types import ModuleType
from typing import List, Optional

import sys

from fhirparser import fhirloader
from fhirparser import fhirspec
from fhirparser.logger import logger

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
    def rel_to_settings_path(opts, path: str) -> str:
        """ Return the absolute path of path relative to the settings directory """
        if os.path.isabs(path):
            return path
        return os.path.abspath(os.path.join(opts.settings_dir, path))

    cwd = os.getcwd()
    opts = genargs().parse_args(args)
    if opts.force and opts.cached:
        raise ArgumentError('force and cached options cannot both be true')
    if os.path.isdir(opts.settings):
        opts.settings = os.path.join(opts.settings, 'settings.py')
    opts.settings_dir = os.path.abspath(os.path.dirname(opts.settings))
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
        settings.tpl_base = rel_to_settings_path(opts, settings.tpl_base)
    logger.info(f"Template directory: {os.path.relpath(settings.tpl_base, cwd)}")
    if opts.outputdir:
        settings.tpl_resource_target = opts.outputdir
    else:
        settings.tpl_resource_target = rel_to_settings_path(opts, settings.tpl_resource_target)
    logger.info(f"Output directory: {os.path.relpath(settings.tpl_resource_target, cwd)}")
    if settings.write_unittests:
        settings.tpl_unittest_target = rel_to_settings_path(opts, settings.tpl_unittest_target)
        logger.info(f"Unit test directory: {os.path.relpath(settings.tpl_unittest_target, cwd)}")
    logger.info(f"Cache directory: {opts.cachedir}")
    loader = fhirloader.FHIRLoader(settings, opts.cachedir)
    spec_source = loader.load(force_download=opts.force, force_cache= opts.cached)
    if not opts.loadonly:
        spec = fhirspec.FHIRSpec(spec_source, settings)
        if not opts.parseonly:
            spec.write()
    return 0

def main() -> int:
    generator(sys.argv[1:])

if '__main__' == __name__:
    sys.exit(main())
