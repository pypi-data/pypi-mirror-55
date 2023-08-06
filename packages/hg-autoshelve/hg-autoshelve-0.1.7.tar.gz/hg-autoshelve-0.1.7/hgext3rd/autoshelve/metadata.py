# Copyright 2019 Alain Leufroy
#                Pythonian <contact@pythonian.fr>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

__all__ = ['__version__', 'testedwith', 'minimumhgversion', 'buglink']

__version__ = b'0.1.7'
testedwith = b'5.1'
minimumhgversion = b'5.1'
buglink = b'https://todo.sr.ht/~alainl/hg-autoshelve'

SYNOPSIS = b'[--noshelve]'

DOCSTRING = b'''
    The autoshelve extension is activated. Dirty working directory
    will be shelved before all then unshelved after all. You
    can use --noshelve to inhibite this behaviour.'''

COMMANDS = [
    b'pull',
    b'backout',
    b'graft', b'merge',
    b'bisect', b'update', b'import', b'unbundle'
]

EXTENSIONS = {
    b'histedit': [b'histedit'],
    b'rebase': [b'rebase'],
    b'evolve': [
        b'prune', b'rewind', b'touch', b'uncommit', b'split', b'pick',
        b'metaedit', b'fold'
    ]
}
__doc__ = """Automatic dirty working directory shelving.

Automatically call `shelve` before a command then `unshelve`
once it's done.

Wrapped commands are {commands}.

A `--noshelve` options is added to them to disable the feature.

The unshelve operation is not performed when the main
command fails. For example, rebasing a commit that results
in conflicts will stop the unshelve operation. You will need
to perform the unshelve manually afterward (`hg unshelve`)

The unshelve operation may results in merge conflict. For example,
updating to a commit onto which the shelved content cannot apply will
results in merge conflicts. You have to:

* fix the conflicts (`hg resolve --mark`) then continue the unshelve
  operation (`hg unshelve --continue`)

* or abort it (`hg unshelve --abort`).

Shelves are named as `autoshelve-RANDOMHEX`, with an `autoshelve-`
prefix flollwed by a random hex. They are removed immediatly, unless
the command fails as explained previously. You can delete them using
`hg shelve --delete --name autoshelve-RADOMEHEX`.
""".format(commands=', '.join(
    "'%s'" % cmd for cmd in sorted(
        COMMANDS + [cmd for cmds in EXTENSIONS.values() for cmd in cmds])))
