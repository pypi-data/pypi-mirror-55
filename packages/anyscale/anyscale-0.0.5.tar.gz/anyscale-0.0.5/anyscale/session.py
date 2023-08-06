import datetime
import click
import logging
import os.path
import tempfile
import time

import ray
import ray.projects.scripts as ray_scripts

from anyscale.util import (confirm, send_json_request)


logging.basicConfig(format=ray.ray_constants.LOGGER_FORMAT)
logger = logging.getLogger(__file__)


class AnyscaleSessionRunner(ray_scripts.SessionRunner):

    def __init__(self, session_id, session_name):
        """Create a new AnyscaleSessionRunner.

        Args:
            session: The ID of the session associated to this run.
        """
        super(AnyscaleSessionRunner, self).__init__()
        self.session_id = session_id
        self.session_name = session_name

        # TODO: We should check that the active session actually matches the
        # created cluster. If the user terminates the cluster out-of-band (through
        # `ray down` instead of `any session stop`), then we won't be able to
        # tell that the session is no longer active.


    def setup_environment(self):
        """Set up the environment of the session."""
        # TODO: Need to make sure this can run without a local copy of the project.
        # super(AnyscaleSessionRunner, self).setup_environment()

        # Install the anyscale client.
        self.execute_command("pip install anyscale")


    def execute_command(self, cmd, config={}, user_command=False):
        """Execute a shell command in the session and add it to the database.

        Args:
            cmd (str): Shell command to run in the session. It will be
                run in the working directory of the project.
            user_command (bool): If True, the command was run explicitly
                by the user.
        """
        if user_command:
            send_json_request("session_execute", {
                "session_id": self.session_id,
                "command": cmd,
                }, post=True)
        return super(AnyscaleSessionRunner, self).execute_command(cmd, config)


    def sync_session(self, snapshot_id, snapshot_directory,
            commit_hash, local_commit_patch, yes):
        """Sync a live session with a snapshot with the given name.

        Args:
            snapshot: The Snapshot to apply.
            snapshot_directory: The local directory with snapshot files to sync
                to the session.
            local_commit_patch: The local location of the patch to apply to the
                remote git repo, if any.
            yes: Don't ask for confirmation.

        Returns:
            The active Session metadata in the database.

        Raises:
            ValueError: If snapshot lookup does not succeed.
        """
        # Sync the git state first.
        if commit_hash is not None:
            # Point the repo to the commit associated with the snapshot.
            self.execute_command(
                "git reset && git checkout . && git checkout {} && git clean -fxd".format(commit_hash))

        # Sync the local directory with snapshot files to the session.
        # NOTE: If the project is not using git, then we will sync all snapshot
        # files correctly, but there may be other files left in the project
        # directory. We can remove them with `rm -r *`, but this seems fishy.
        snapshot_directory = os.path.join(snapshot_directory, "")
        ray_scripts.rsync(
            self.project_definition.cluster_yaml(),
            source=snapshot_directory,
            target=self.project_definition.working_directory(),
            override_cluster_name=self.session_name,
            down=False,
        )

        # Apply the git diff to the session's project directory, if any.
        if local_commit_patch is not None:
            # Remove the patch after applying.
            self.execute_command(
                    "git apply {} && rm {}".format(local_commit_patch, local_commit_patch))

        # Ask the server to record that this snapshot was synced.
        send_json_request("session_sync", {
            "session_id": self.session_id,
            "snapshot_id": snapshot_id,
            }, post=True)
