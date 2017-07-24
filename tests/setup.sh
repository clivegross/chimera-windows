#!/bin/bash

APPNAME=chimera
APPFULLNAME="$APPNAME Linux client"
VERSION="0.1"
AUTHOR="Clive Gross, Typhon Solutions Pty Ltd"

# path variables
APPDIR="/opt/$APPNAME"
BINDIR="$APPDIR/bin"
VARDIR="/var/opt/$APPNAME"
ETCDIR="/etc/opt/$APPNAME"
JOBDIR="$ETCDIR/jobs"
LOGDIR="/var/logs/$APPNAME"
LOG="backups.log"
SYSTEMDDIR="/lib/systemd/system"
INSTALLDIR=$(pwd)

APPURL="https://gitlab.com/TyphonSolutions/chimera/bdr-linux-client/repository/archive.zip?ref=master"

RCLONEPACKAGE="rclone-current-linux-arm.zip"
RCLONEURL="https://downloads.rclone.org/$RCLONEPACKAGE"

HEADLINE="###########################################################################################"

echo ""
echo $HEADLINE
echo "Installing $APPFULLNAME"
echo "Version: $VERSION"
echo "Author: $AUTHOR"

echo ""
echo $HEADLINE
echo ""
echo "Downloading rclone..."
curl -O $RCLONEURL
echo "Done."
echo ""
echo "Unzipping rclone..."
unzip $RCLONEPACKAGE
cd rclone-*-linux-arm
echo $(pwd)
echo "Done."
echo ""
echo "Copying rclone application files..."
#
# cp rclone /usr/bin/
# # chown root:root /usr/bin/rclone
# chmod 755 /usr/bin/rclone
# mkdir -p /usr/local/share/man/man1
# cp rclone.1 /usr/local/share/man/man1/
cd $INSTALLDIR
echo $(pwd)
echo "Done."

echo ""
echo $HEADLINE
echo "Downloading $APPNAME..."
curl -o $APPNAME-installer.zip $APPURL
echo "Done."
echo "Unzipping $APPNAME..."
unzip $APPNAME-installer.zip
cd $APPNAME
echo $(pwd)
echo "Done."
echo "Copying $APPNAME) application files..."
# mkdir -p $APPDIR
# mkdir -p $BINDIR
# chmod -R +x $BINDIR
# mkdir -p $VARDIR
# mkdir -p $ETCDIR
# mkdir $ETCDIR/examples/jobs
# mkdir -p $JOBDIR
# mkdir -p $LOGDIR
# touch "$LOGDIR/$LOG"
# chmod -R 664 $LOGDIR

echo "Copying configuration files..."
# cp examples/config.ini $ETCDIR
echo "Done."
echo "Copying examples..."
# cp examples/* $ETCDIR/examples
# cp examples/jobs/* $ETCDIR/examples/jobs
echo "Done."

echo "Copying application files and binaries..."
# cp -rv * $APPDIR
echo "Done."

echo ""
echo $HEADLINE
echo "Configuring systemd..."
# cp -v $APPNAME.service $SYSTEMDDIR
# chmod + x $SYSTEMDDIR/$APPNAME.service
# systemctl enable $APPNAME.service
cd $INSTALLDIR
echo $pwd
echo "Done."

echo ""
echo $HEADLINE
echo "Updating mandb"
# mandb
echo "Done."

echo ""
echo $HEADLINE
echo "Cleaning up"
echo $(pwd)
rm rclone*.zip
rm -r rclone-*-linux-arm
rm -r $APPNAME-installer
rm -r $APPNAME-installer.zip
echo "Done."

echo ""
echo $HEADLINE
echo "Installation complete! Create jobs in the $JOBDIR, refer to $ETCDIR/examples for help getting started."
echo ""
echo "chimera.service has been enabled under systemd. Once configuration is complete, start the service:"
echo ""
echo "    systemctl start chimera.service"
