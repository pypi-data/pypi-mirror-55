# -*- coding: utf-8 -*-

"""Console script for cronshield."""
import random
import subprocess
import sys
import time
from pathlib import Path

import click


@click.command()
@click.option(
    "--error-touchfile",
    type=click.Path(dir_okay=False),
    help="If present, the mtime of this file is updated to the current time."
)
@click.option(
    "--max-failure-interval",
    type=int,
    metavar="SECONDS",
    default=sys.maxsize,
    help=(
             "Maximum error interval that is reported.  If an error occurs with a greater interval than this, it is "
             "ignored.  --error-touchfile must be specified if this is provided."
    )
)
@click.option(
    "--report-probability",
    type=float,
    metavar="PROBABILITY",
    default=1.0,
    help=(
             "Probability that an error is reported.  Setting this to 0.5, for example, will mask half of the actual "
             "errors."
    )
)
@click.argument("command", nargs=-1, required=True, type=str)
def main(command, error_touchfile, max_failure_interval, report_probability):
    """Console script for cronshield."""
    if max_failure_interval != sys.maxsize and error_touchfile is None:
        print(f"--max-failure-interval requires --error-touchfile to be set.", file=sys.stderr)
        sys.exit(2)

    process = subprocess.run(args=command, capture_output=True)

    if process.returncode == 0:
        sys.exit(0)

    try:
        if error_touchfile is not None:
            error_touchfile_path = Path(error_touchfile)

            try:
                # do we report this error?
                now = time.time()
                if max_failure_interval != sys.maxsize and error_touchfile_path.exists():
                    last_error_mtime = error_touchfile_path.stat().st_mtime

                    if now - last_error_mtime > max_failure_interval:
                        # last error was way too long ago.
                        return
            finally:
                error_touchfile_path.touch()

        rand_value = random.random()
        if rand_value >= report_probability:
            return

        command_text = " ".join(command)

        print(f"cronshield detected failure or error output for the command: {command_text}")
        print(f"")
        print(f"RESULT CODE: {process.returncode}")
        if len(process.stdout) > 0:
            print(f"")
            print(f"OUTPUT:")
            print(f"{process.stdout.decode('latin-1')}")
        if len(process.stderr) > 0:
            print(f"")
            print(f"ERROR:")
            print(f"{process.stderr.decode('latin-1')}")
    finally:
        sys.exit(process.returncode)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
