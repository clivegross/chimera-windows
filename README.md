# Chimera Linux client

## License
[GNU GENERAL PUBLIC LICENSE Version 3](./LICENSE)

## Description
Has the following possible uses:
- Run as an onsite backup agent for [chimera cloud](https://chimeracloud.io).
- Run as a standalone service for automating scheduled backup jobs using [rclone ](https://rclone.org/).

## Quickstart
### Installation
Run setup.sh or read the contents of the script to see what must be done.

### Configuration
Configuration workflow is roughly as follows:
1. Configure remote in rclone
2. Configure main config file
3. Configure backup job config files
4. Start/enable systemd service

#### Configure rclone
Set up a remote using `rclone config`.

Refer to [rclone docs](https://rclone.org/docs/).

chimera does not currently support password protected rclone config.

#### Point chimera to config files
chimera will look for the main config file and job config files, resepectively, by default in:

```
/etc/opt/chimera/config.ini
/etc/opt/chimera/jobs/*.ini

```

These path settings can be changed in the main app `paths.ini` file.

#### Main config
Configure the main config file:

```
[email]
sender: support@example.com
recipients: me@example.com
host: smtp.example.com
port: 587
username: Me
password: My password
enabled: True

[rclone]
remote: backup-gdrive

[logging]
file: /var/log/chimera/backups.log
enabled: True

```

#### Configure backup jobs
Currently, the supported method of configuring backup jobs is by describing the job in an ini config file in the jobs directory. Support is coming for json and a web UI.

Chimera will read in all `*.ini` files in the jobs dir, multiple jobs can live in a single file, where each section is a job or a separate file per job. The section title for a job must start with `job`.

```
[job example job name]
source: /data/Documents/backups/test02dir
dest: my/Google Drive/backups/folder/test02dir
schedule: 0 * * * *
enabled: True
append_datetime: True
sync: False
compress: True

```

Options:
- source: the path to the source backup file/dir
- dest: the path to the remote destination file/dir
- schedule: a cron-like representation of the backup schedule
- enabled: whether the backup job is enabled
- append_datetime (optional, default True): whether to append "_YYYYmmdd_HHMMSSffffff" to the end of the file/dir name
- sync (optional, default False): whether to mirror source to remote using rclone sync instead of rclone copy
- compress (optional, default False): compress source to a zip file before upload

## Dependencies
- rclone
- python 2.7 (python 3.x should work with some minor fixes)
- systemd for running as a service (optional)
