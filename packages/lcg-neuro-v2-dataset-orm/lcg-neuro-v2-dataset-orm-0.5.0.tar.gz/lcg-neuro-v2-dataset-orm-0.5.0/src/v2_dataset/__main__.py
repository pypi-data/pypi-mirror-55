"""Command-line tools to obtain information about the V2 dataset and its files.
"""

import attr
import click
import os
import plx
import subprocess
import sys
import tempfile

from pathlib import Path
from v2_dataset import model, parsing
from v2_dataset.db import config as db_config, Database


@attr.s
class Context:
    db: Database = attr.ib()
    init: bool = attr.ib()


@click.group(help=__doc__.split(".")[0])
@click.option(
    "--db",
    "db_path",
    default=None,
    type=click.types.Path(
        file_okay=True, dir_okay=False, writable=True, readable=True, resolve_path=True
    ),
    help="Path to database file. Whether it will be created and initialized, if it does not already exist, is affected by the V2_DATASET_DB_AUTO_INIT environment variable or the -i switch.",
)
@click.option(
    "--init",
    "-i",
    is_flag=True,
    default=False,
    help="Turn on automatic initialization of the database, if it does not exist already. This has precedence over the V2_DATASET_DB_AUTO_INIT environment variable.",
)
@click.pass_context
def main(ctx, db_path, init):
    db_path = Path(db_path or db_config.path)
    init = (init or db_config.auto_init) and not db_path.exists()
    db = Database(f"sqlite:///{db_path}", init=init)

    ctx.obj = Context(db=db, init=init)


@main.command(
    name="init",
    help="Initialize a database file with curated information only. This command always tries to initialize a fresh database, irrespective of whether it already exists and of the presence of the --init flag and of the V2_DATASET_DB_AUTO_INIT environment variable's value. If the database already exists and has been previously initialized, this command will fail, unless the -w switch is passed.",
)
@click.option(
    "-w",
    "--overwrite",
    is_flag=True,
    default=False,
    help="Force initialization of database. If it already exists, it will be erased before.",
)
@click.pass_obj
def main_init(ctx, overwrite):
    # TODO: Make tests for these cases: init command succeeds only on non-existing file, or non-initialized existing file, or on -w.
    if overwrite:
        # TODO: This could be a method in the db object.
        model.core.Model.metadata.drop_all(ctx.db.engine)
        ctx.db.init()
        ctx.init = True
    elif not ctx.init:
        ctx.db.init()
        ctx.init = True


@main.group(name="recording", help="Manipulate dataset recordings.")
def main_recording():
    pass


@main_recording.command(
    name="parse",
    help="Parse the PLX file of an existing recording, generating trial and spike "
    "channel objects, that are added to the database.",
)
@click.option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="Do not commit changes to the DB (but produces export files).",
)
@click.option(
    "--id",
    "-i",
    "ids",
    multiple=True,
    type=int,
    help="ID of target dataset recording. May be specified " "multiple times.",
)
@click.option(
    "-p",
    "--plx-path",
    default=None,
    type=click.types.Path(readable=True, file_okay=True, dir_okay=False),
    help="Manually specify path to corresponding PLX file. If not specified, it is searched for in the default dataset"
    " directories.",
)
@click.option(
    "--overwrite-exports", "-w", is_flag=True, help="Overwrite exported PLX parts."
)
@click.option(
    "--use-exported", "-x", is_flag=True, help="Assume the PLX file was pre-exported."
)
@click.pass_obj
def main_recording_parse(
    ctx: Context, dry_run, ids, overwrite_exports, use_exported, plx_path
):

    session = ctx.db.session()

    for id in ids:
        click.echo(f"Opening database session and retrieving recording with ID={id}...")
        recording = session.query(model.Recording).filter_by(id=id).one()
        if plx_path is None:
            plx_path = recording.path

        if use_exported:
            export_dir = plx_path.parent / "export"
            click.echo(f'Using pre-exported PLX file at "{export_dir!s}"...')
            plx_file = plx.ExportedPlxFile(export_dir)
        else:
            click.echo(f'Exporting PLX file "{recording.path!s}"...')
            if overwrite_exports:
                plx_file = plx.PlxFile(plx_path).export_file()
            else:
                plx_export_dir = tempfile.TemporaryDirectory(
                    prefix=f"{__name__}_recording_parse_{id}.", suffix=".export"
                )
                plx_file = plx.PlxFile(
                    plx_path, export_base_dir=plx_export_dir.name
                ).export_file()

        click.echo("Parsing spike channels and embedded sorting...")
        parsing.parse_spike_channels(recording, session, plx_file)

        click.echo("Parsing trials...")
        parsing.parse_trials(recording, session, plx_file)

    if dry_run:
        click.echo("Reverting changes to database...")
        session.rollback()
    else:
        click.echo("Committing changes to database...")
        session.commit()

    session.close()
    click.echo("Done.")


@main_recording.command(name="get-plx")
@click.argument("id", type=int)
@click.option("--remote", "-r", help="Name of rclone remote", default="lcg_drive")
@click.option(
    "--force", is_flag=True, default=False, help="Download the file even if it exists."
)
@click.pass_obj
def main_recording_get_plx(ctx: Context, id, remote, force):
    """Download a PLX file of specified ID from the original *V2 Dataset* using *rclone*.

    This is a development command, and should be used with a copy of the V2 Dataset's `contents repository`_.

    .. rubric:: Steps

    1. Get a connection with the :mod:`v2_dataset.db database
    2. Obtain one of the `V2 Dataset`_ PLX paths for the recording with the specified ID
    3. Check if the destination exists (abort, if it does, unless ``--force`` is passed)
    4. Download the PLX file from the `V2 Dataset`_ using `rclone`_ into the dataset directory
       (:attr:`v2_dataset.dbconfig.dataset_dir <v2_dataset.dbconfig.config.dataset_dir>`)
    6. Print Git commands that should be run to finish the changes

    .. important::

        This command requires `rclone`_ to be installed, and at least one remote (the default one) with access to the
        `LCG Neuroscience folder`_ must configured.

    .. _LCG Neuroscience folder: https://drive.google.com/drive/u/0/folders/1UieuXEmeroAteDgu7VvN1oJW7mc5o2YB
    .. _V2 Dataset: https://gitlab.com/lcg/neuro/v2/dataset/contents
    .. _rclone: https://rclone.org/
    """
    dataset_path = Path("Neuroscience/Datasets/ProjectV2/latest/data")

    session = ctx.db.session()
    recording = session.query(model.Recording).filter_by(id=id).one()

    dataset_plx_path = recording.paths[0].as_path()

    remote_plx_path = f"{remote}:{dataset_path!s}/{dataset_plx_path!s}"
    local_dest_path = recording.path
    local_rclone_dest_path = local_dest_path.parent / dataset_plx_path.name
    if local_dest_path.exists():
        if force:
            click.echo(
                f"WARNING: Destination exists, but overriding (--force): {local_dest_path!s}"
            )
        else:
            click.echo(f"ERROR: Destination exists: {local_dest_path!s}")
            sys.exit(1)
    rclone_command = f"rclone copy -v {remote_plx_path} {local_dest_path.parent}"

    click.echo(f"Creating directory: {local_dest_path.parent!s}")
    local_dest_path.parent.mkdir(parents=True, exist_ok=True)

    click.echo(rclone_command)
    rclone_process = subprocess.Popen(
        rclone_command.split(),
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
        bufsize=1,
    )
    rclone_process.wait()

    if rclone_process.returncode == 0:
        click.echo(f"Finished copying file: {local_rclone_dest_path!s}")

        click.echo(f'Renaming file: "{local_rclone_dest_path}" -> "{local_dest_path}"')
        local_rclone_dest_path.rename(local_dest_path)

        try:
            session.add(recording)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        click.echo(f"You should now call")
        click.echo(f'    dvc  add "{local_dest_path.parent!s}"')
        click.echo(f'    git commit -am "Added PLX file (ID={id}) to DVC"')
        click.echo(f'    dvc push "{local_dest_path.parent!s}"')
        click.echo(f"to commit and synchronize changes.")

    session.rollback()
    session.close()


@main_recording.command(name="info")
@click.option(
    "--id",
    "-i",
    "ids",
    multiple=True,
    type=int,
    help="Specify a recording by its dataset ID (may be " "specified multiple times).",
)
@click.option("--path", is_flag=True, help="Print the path of every selected file.")
@click.pass_obj
def main_recording_info(ctx: Context, ids, path):
    """Print information about PLX files in the dataset.

    \f
    :param List[int] ids:
    :param bool path:
    """
    session = ctx.db.session()
    for plx_id in ids:
        plx_path = session.query(model.Recording).filter_by(id=plx_id).one().path
        if path:
            plx_rel_path = os.path.relpath(plx_path, os.getcwd())
            click.echo(plx_rel_path)
    session.rollback()
    session.close()


if __name__ == "__main__":
    main(prog_name=f'python -m {__package__.replace("__main__", "")}')
