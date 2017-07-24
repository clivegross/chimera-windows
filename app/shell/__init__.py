import subprocess


def shell_command(command, std_as_str=True):
    """
    execute <command> as shell command using subprocess
    use --config switch to explicitly set config file.
    When managed by systemd, chimera cant find the rclone config file
    """
    # bash command
    # use --config switch to set config file.
    # When systemd managed by systemd, chimera cant find rclone config file
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # output equals tuple (stdout, stderr)
    # note stderr isnt necessarily error output,
    # may contain standard verbose output from rclone
    output = process.communicate()
    if std_as_str:
        output = concat_std(output)
    return output


def concat_std(std_tuple):
    """
    Popen returns a tuple (stdout, stderr)
    concatenate output into a single string
    """
    std_str = '\n'.join([
    'stdout:',
    str(std_tuple[0]),
    'stderr:',
    str(std_tuple[1])
    ])
    return std_str
