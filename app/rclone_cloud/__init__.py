from app.shell import shell_command


class Cloud(object):
    """
    a simple wrapper for rclone
    """

    def __init__(self, remote, bucket=None, config=None):
        """
        remote: name of rclone remote cloud store
        """
        self.str_checker(remote)
        self.set_remote(remote, bucket)
        self.config = config

    def set_remote(self, remote, bucket=None):
        self.remote = remote + ':'
        if bucket:
            self.remote += str(bucket)

    def is_str(self, obj):
        """
        check if object is a string
        """
        if isinstance(obj, str):
            return True
        else:
            return False

    def str_checker(self, obj):
        """
        raise exception if the object is not a string
        """
        if not self.is_str(obj):
            raise TypeError("object must be a string, " + str(type(obj)) + " was given")

    def bash_command(self, command, std_as_str=True):
        """
        execute <command> as bash command using subprocess
        use --config switch to explicitly set config file.
        When managed by systemd, chimera cant find the rclone config file

        TODO:
        * test this works ince importing shell_command

        """
        # bash command
        # use --config switch to set config file.
        # When systemd managed by systemd, chimera cant find rclone config file
        if self.config is not None:
            command.insert(2, "--config=" + self.config)
        output = shell_command(command, std_as_str)
        return output

    def concat_std(self, std_tuple):
        """
        Popen returns a tuple (stdout, stderr)
        concatenate output into a single string
        """
        std_str = '\n'.join([
        'stdout:',
        std_tuple[0],
        'stderr:',
        std_tuple[1]
        ])
        return std_str

    def lsd(self, path=None):
        """
        wrapper for rclone lsd
        https://rclone.org/commands/rclone_lsd/
        execute:
        rclone lsd <remote>/<path>
        """
        if path is None:
            path_checked = ""
        else:
            self.str_checker(path)
            path_checked = path
        # bash command
        command = ["rclone",  "lsd", self.remote + "/" + path_checked]
        output = self.bash_command(command)
        return output

    def copy(self, source, dest_path, verbose=True):
        """
        wrapper for rclone copy
        https://rclone.org/commands/rclone_copy/
        execute:
        rclone copy <source> <remote>/<dest_path>
        """
        self.str_checker(source)
        self.str_checker(dest_path)
        dest = self.remote + "/" + dest_path
        command = ["rclone", "copy", "-v", source, dest]
        if not verbose:
            del command[2]
        output = self.bash_command(command)
        return output

    def sync(self, source, dest_path, verbose=True):
        """
        wrapper for rclone sync
        https://rclone.org/commands/rclone_sync/
        execute:
        rclone sync <source> <remote>/<dest_path>
        """
        self.str_checker(source)
        self.str_checker(dest_path)
        dest = self.remote + "/" + dest_path
        command = ["rclone", "sync", "-v", source, dest]
        if not verbose:
            del command[2]
        output = self.bash_command(command)
        return output
