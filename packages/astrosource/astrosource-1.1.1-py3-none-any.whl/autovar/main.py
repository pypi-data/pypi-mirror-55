from pathlib import Path
import click
import sys
import logging

from numpy import array

from astrosource.identify import find_stars, gather_files
from astrosource.comparison import find_comparisons, find_comparisons_calibrated
from astrosource.analyse import calculate_curves, photometric_calculations
from astrosource.plots import make_plots, phased_plots
from astrosource.eebls import plot_bls
from astrosource.detrend import detrend_data
from astrosource.periodic import plot_with_period

from astrosource.utils import get_targets, folder_setup, AstrosourceException, cleanup


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option('--full', is_flag=True)
@click.option('--stars', is_flag=True)
@click.option('--comparison', is_flag=True)
@click.option('--calc', is_flag=True)
@click.option('--calib', is_flag=True)
@click.option('--phot', is_flag=True)
@click.option('--plot', is_flag=True)
@click.option('--detrend', is_flag=True)
@click.option('--eebls', is_flag=True)
@click.option('--indir', default=None, type=str, required=True)
@click.option('--ra', type=float)
@click.option('--dec', type=float)
@click.option('--target-file', default=None, type=str)
@click.option('--format', default='fz', type=str)
@click.option('--clean', is_flag=True)
def main(full, stars, comparison, calc, calib, phot, plot, detrend, eebls, indir, ra, dec, target_file, format, clean):
    try:
        parentPath = Path(indir)
        if clean:
            cleanup(parentPath)
            logger.info('All temporary files removed')
            return
        if not (ra and dec) and not target_file:
            logger.error("Either RA and Dec or a targetfile must be specified")
            return

        paths = folder_setup(parentPath)
        filelist, filtercode = gather_files(paths, filetype=format)

        if ra and dec:
            targets = array([(ra,dec,0,0)])
        elif target_file:
            target_file = parentPath / target_file
            targets = get_targets(target_file)

        # sys.tracebacklimit = 0

        if full or stars:
            usedimages = find_stars(targets, paths, filelist)
        if full or comparison and not calib:
            find_comparisons(parentPath)
        if full or comparison and calib:
            find_comparisons_calibrated(filtercode, paths)
        if full or calc:
            calculate_curves(targets, parentPath=parentPath)
        if full or phot:
            photometric_calculations(targets, paths=paths)
        if full or plot and not detrend and not calib:
            make_plots(filterCode=filtercode, paths=paths)
        if detrend:
            detrend_data(paths, filterCode=filtercode)
        if eebls:
            plot_bls(paths=paths)
        if calib:
            plot_with_period(paths, filterCode=filtercode)
        logger.info("Completed analysis")

    except AstrosourceException as e:
        logger.critical(e)

if __name__ == '__main__':
    main()
