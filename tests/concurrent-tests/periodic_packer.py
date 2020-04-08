#!/usr/bin/env python
import time

import click

from disk_objectstore.container import Container

@click.command()  # noqa: MC0001
@click.option('-p', '--path', default='/tmp/test-container', help='The path to a test folder in which the container will be created.')
@click.option('-r', '--repetitions', default=10, help='Number of repetitions before stopping.')
@click.option('-w', '--wait-time', default=0.83, help='Time to wait between iterations.')
@click.option('-z', '--compress-packs', is_flag=True, help='Compress objects while packing.')
@click.help_option('-h', '--help')
def main(path, repetitions, wait_time, compress_packs): # pylint: disable=too-many-arguments,too-many-locals,too-many-statements,too-many-branches
    """Periodically pack container."""
    container = Container(path)
    if not container.is_initialised:
        raise ValueError("Can only pack initialised containers.")

    for iteration in range(repetitions):
        if iteration != 0:
            time.sleep(wait_time)

        start_counts = container.count_objects()
        container.pack_all_loose(compress=compress_packs)
        print("[PACKER] Done packing!")
        end_counts = container.count_objects()

        print("[PACKER] Packed objects (was {} loose, {} packed; now: {} loose, {} packed).".format(
            start_counts['loose'], start_counts['packed'], end_counts['loose'], end_counts['packed']))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter