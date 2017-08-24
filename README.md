# Chimera for Windows

## License
[GNU GENERAL PUBLIC LICENSE Version 3](./LICENSE)

## Description
Has the following possible use cases:
- ~~Run as an onsite backup agent for [Chimera Cloud Backup and Disaster Recovery](https://chimeracloud.io).~~ (not yet supported)
- Run as a standalone service for automating scheduled backup jobs on any Windows machine. Can backup to any of the following storage services:
  * Amazon S3
  * Google Drive
  * Openstack Swift / Rackspace cloud files / Memset Memstore
  * Dropbox
  * Google Cloud Storage
  * Amazon Drive
  * Microsoft OneDrive
  * Hubic
  * Backblaze B2
  * Yandex Disk
  * SFTP
  * FTP
  * HTTP

## Quickstart
### Installation
Download the latest version of Chimera from [here](https://github.com/clivetyphon/chimera-windows/releases).

### Configuration
Configuration workflow is roughly as follows:
1. Configure main config file
2. Configure backup job config files
3. Install and start the Windows service.

#### Configure rclone
Set up a remote using `rclone config`.

Refer to [rclone docs](https://rclone.org/docs/).

chimera does not currently support password protected rclone config.

#### Point chimera to config files
chimera will look for the main config file and job config files, resepectively, by default in:

```
C:\Program Files/Chimera/Chimera Backup Agent/config.ini
C:\Program Files/Chimera/Chimera Backup Agent//jobs/*.ini
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

[remote]
...

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
- NSSM
