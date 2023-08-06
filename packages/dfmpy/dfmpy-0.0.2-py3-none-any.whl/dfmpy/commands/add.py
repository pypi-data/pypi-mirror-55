# TODO docs

from logging import getLogger
from os.path import expanduser
from os.path import expandvars
from pathlib import Path

# TODO remove dependency on other commands.
from dfmpy.commands.sync import __sync_expected_paths
from dfmpy.utils.config import get_config
from dfmpy.utils.files import mkdir_parents
from dfmpy.utils.files import path_exists

LOG = getLogger()


def __normalize_file_names(files):
    # TODO docs
    # TODO unit test
    if not files:
        files = []
    files = [expanduser(expandvars(f)) for f in files]
    files = [Path(f).absolute() for f in files]
    return tuple(files)


def __filter_non_destination_paths(paths):
    # TODO docs
    # TODO unit test
    install_dir = get_config().install_dir
    good_paths = []
    for p in paths:
        if not path_exists(p):
            LOG.error('Cannot add non-existent path: %s', p)
        elif not str(p).startswith(install_dir):
            LOG.error('Cannot add path not under destination: %s', p)
        else:
            good_paths.append(p)
    return tuple(good_paths)


def __determine_expected_paths(paths):
    # TODO docs
    # TODO unit test
    repository = get_config().repository
    install_dir = get_config().install_dir
    marker = get_config().marker
    hostname = get_config().hostname
    expected_paths = {}
    for p in paths:
        target_path = \
            str(p).replace(install_dir, repository) + marker + hostname
        expected_paths[p] = Path(target_path)
    return expected_paths


def __move_expected_paths(expected_paths, force):
    # TODO docs
    # TODO unit test
    for old, new in expected_paths.items():
        if not force:
            LOG.info('Simulated renaming %s -> %s', old, new)
        else:
            mkdir_parents(new)
            LOG.info('Renaming %s -> %s', old, new)
            Path(old).rename(new)


def add(files=None, force=False, interactive=False):
    # TODO do not overwrite existing files
    # TODO docs
    # TODO unit test
    # TODO implement interactive
    # TODO implement force
    paths = __normalize_file_names(files)
    paths = __filter_non_destination_paths(paths)
    expected_paths = __determine_expected_paths(paths)
    __move_expected_paths(expected_paths, force)
    # TODO make this the next method public, or move to the "files" utility?
    __sync_expected_paths(expected_paths, force, interactive)
    # if interactive:
    #     raise NotImplementedError('Interactive not yet implemented.')
    # __install_file('config.ini', overwrite=force)
    # __install_file('ignore.globs', overwrite=force)


def add_main(cli):
    # TODO docs
    # TODO unit test
    add(cli.files,
        cli.force,
        cli.interactive)
