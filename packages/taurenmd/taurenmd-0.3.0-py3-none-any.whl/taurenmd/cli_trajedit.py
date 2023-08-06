"""
Edit a trajectory.

File format, length (that is, frames) and selection can be edited.

Uses MDAnalsysis.
"""
import argparse

import MDAnalysis as mda

from taurenmd import Path, log
from taurenmd.libs import libmda
from taurenmd.logger import S, T


ap = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

ap.add_argument(
    'topology',
    help='Topology file.',
    type=str,
    )

ap.add_argument(
    'trajectory',
    help=(
        'Trajectory files. If given, multiple trajectories will be'
        'contactenated by order.'
        ),
    nargs='+',
    )

ap.add_argument(
    '-s',
    '--start',
    help='Start frame for slicing.',
    default=None,
    type=int,
    )

ap.add_argument(
    '-e',
    '--stop',
    help='Stop frame for slicing: exclusive',
    default=None,
    type=int,
    )

ap.add_argument(
    '-p',
    '--step',
    help='Step value for slicing',
    default=None,
    type=int,
    )

ap.add_argument(
    '-l',
    '--selection',
    help='Atom selection. Read: https://www.mdanalysis.org/docs/documentation_pages/selections.html',  # noqa: E501
    default='all',
    type=str,
    )

ap.add_argument(
    '-d',
    '--traj-output',
    help='Edited trajectory.',
    default='traj_output.xtc',
    type=Path,
    )

ap.add_argument(
    '-o',
    '--top-output',
    help="Topology output first frame.",
    type=Path,
    default='top_output.pdb',
    )

ap.add_argument(
    '-t',
    '--no-top',
    help='If given, does not create topology for the first frame.',
    action='store_true',
    )


def load_args():
    cmd = ap.parse_args()
    return cmd


def maincli():
    cmd = load_args()
    main(**vars(cmd))
    return


def main(
        topology,
        trajectory,
        start=None,
        stop=None,
        step=None,
        selection='all',
        traj_output='traj_output.xtc',
        top_output='top_output.pdb',
        no_top=False,
        **kwargs
        ):
   
    log.info(T('editing trajectory'))

    u = libmda.mda_load_universe(topology, *list(trajectory))
    
    log.info(S('slicing: {}::{}::{}', start, stop, step))
   
    log.info(S('selecting: {}', selection))
    selection = u.select_atoms(selection)
    log.info(S('with {}', selection.n_atoms, indent=2))
   
    traj_output = Path(traj_output)
    log.info(S('saving to: {}', traj_output.resolve().str()))
    with mda.Writer(traj_output.str(), selection.n_atoms) as W:
        for ts in u.trajectory[slice(start, stop, step)]:
            W.write(selection)
   
    if not no_top:
        log.info(S('saving first frame to: {}', top_output))
        with mda.Writer(Path(top_output).str(), selection.n_atoms) as W:
            for ts in u.trajectory[0:1]:
                W.write(selection)
    else:
        log.info(S('topology not written'))
   
    log.info(S('Done'))
    return


if __name__ == '__main__':
    maincli()
