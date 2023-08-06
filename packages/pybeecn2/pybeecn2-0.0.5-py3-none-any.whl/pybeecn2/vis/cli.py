"""
This work was authored by Gabriel McBride in support
of Portland Open Data Program and Portland Bureau of
Emergency Management BEECN Program. The effort was
conducted as a use case for the student's masters
project to study the interaction between Systems
Engineering and Data Science activities.
"""

import argparse
from pybeecn2.vis.run import main


def setup_beecn_parser(subp, parents):
    """
    """
    # Create the parser
    parser = subp.add_parser('map', formatter_class=argparse.RawDescriptionHelpFormatter,
                             description=setup_beecn_parser.__doc__,
                             help='view the locations of BEECN sites', parents=parents)

    # Add arguments to the parser
    parser.add_argument('--show',
                        default=False,
                        action='store_true',
                        help='show the plots during runtime')
    parser.add_argument('--directory',
                        required=True,
                        help='directory where to store the files generated from the analysis')
    parser.add_argument('--boundaries',
                        required=True,
                        help='Geographic boundaries for the map to plot')
    parser.add_argument('--points',
                        required=True,
                        help='The points to add to the map')
    parser.set_defaults(func=main)

def __argparse__(subp, parents=[]):
    """PyBEECN2 Application
    The PyBEECN2 application in it's initial design is built to provide an interface
    in which the user can look at the distribution of 1. the total population of
    Portland, OR 2. The various Limited English Speaking populations of Portland, OR
    and 3. The distribution of BEECN sites across Portland, OR. The data used
    in the application comes from Portland Open data and is as current as the
    source advertises.
    """

    setup_beecn_parser(subp, parents)

