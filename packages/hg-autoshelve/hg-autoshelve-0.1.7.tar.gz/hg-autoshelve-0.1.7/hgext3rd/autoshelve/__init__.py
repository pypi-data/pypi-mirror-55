# Copyright 2019 Alain Leufroy
#                Pythonian <contact@pythonian.fr>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import random
from functools import partial

from mercurial import cmdutil, commands, extensions
from mercurial.i18n import _

from . import metadata

__version__ = metadata.__version__
__doc__ = metadata.__doc__
testedwith = metadata.testedwith
minimumhgversion = metadata.minimumhgversion
buglink = metadata.buglink


def extsetup(ui):
    for cmd in metadata.COMMANDS:
        _wrap_cmd(commands.table, cmd)
    for extension, cmds in metadata.EXTENSIONS.items():
        _uisetup_extension(extension, cmds)


def _uisetup_extension(name, cmds):
    extensions.afterloaded(
        name,
        partial(_wrap_extension_cmd, name=name, cmds=cmds)
    )


def _wrap_extension_cmd(name, cmds, loaded=None):
    try:
        extension = extensions.find(name)
    except KeyError:
        return
    for cmd in cmds:
        _wrap_cmd(extension.cmdtable, cmd)


def _wrap_cmd(table, cmd):
    entry = extensions.wrapcommand(
        table, cmd, _autoshelve_cmd,
        synopsis=metadata.SYNOPSIS, docstring=metadata.DOCSTRING
    )
    entry[1].append(
        (b'', 'noshelve', None, _(b'Disable autoshelve')))


def _autoshelve_cmd(orig, ui, repo, *values, **opts):
    shelve_name = _generate_shelve_name(15)
    shelved = False
    if not opts.get('abort') and not opts.pop('noshelve', False):
        shelved = _shelve(ui, repo, shelve_name) is None
    output = orig(ui, repo, *values, **opts)
    if shelved:
        _unshelve(ui, repo, shelve_name)
    return output


def _generate_shelve_name(length):
    urandom = random.SystemRandom()
    str_format = 'autoshelve-%%0%dx' % length
    return str_format % urandom.getrandbits(length * 4)


def _shelve(ui, repo, shelve_name):
    _alias, shelvecmd = cmdutil.findcmd(b'shelve', commands.table)
    return shelvecmd[0](ui, repo, name=shelve_name, keep=False)


def _unshelve(ui, repo, shelve_name):
    _alias, unshelvecmd = cmdutil.findcmd(b'unshelve', commands.table)
    unshelvecmd[0](ui, repo, name=shelve_name, keep=False)
