#!/bin/bash
# Action1 - Linux System Disk Encryption
#
# Checks whether the filesystem containing /
# is backed by a dm-crypt/LUKS encrypted device.
#
# Output:
# SystemDiskEncrypted=Yes/No/Unknown

ROOT_SOURCE=$(findmnt -n -o SOURCE / 2>/dev/null)

# Cannot determine root filesystem
if [ -z "$ROOT_SOURCE" ]; then
    echo "SystemDiskEncrypted=Unknown"
    exit 0
fi

ENCRYPTED="No"

# Check the complete block-device hierarchy beneath the root filesystem.
# This handles common configurations such as:
#
#   LUKS -> filesystem
#   LUKS -> LVM -> filesystem
#   LUKS -> LVM -> root logical volume

if lsblk -s -n -o TYPE "$ROOT_SOURCE" 2>/dev/null | grep -qx "crypt"; then
    ENCRYPTED="Yes"
fi

echo "SystemDiskEncrypted=$ENCRYPTED"

# Always exit successfully for Action1
exit 0