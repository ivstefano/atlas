#!/bin/bash

# Action1 - Automatic Screen Lock Status (Linux / GNOME)

endpoint=$(hostname)
user=""

# Find active graphical session
if command -v loginctl >/dev/null 2>&1; then
    while read -r sid _; do
        type=$(loginctl show-session "$sid" -p Type --value 2>/dev/null)
        active=$(loginctl show-session "$sid" -p Active --value 2>/dev/null)

        if [ "$active" = "yes" ] && \
           { [ "$type" = "x11" ] || [ "$type" = "wayland" ]; }; then

            user=$(loginctl show-session "$sid" -p Name --value 2>/dev/null)
            break
        fi
    done < <(loginctl list-sessions --no-legend 2>/dev/null)
fi

if [ -z "$user" ]; then
    echo "Endpoint=$endpoint; ScreenLockEnabled=Unknown; IdleTimeSeconds=Unknown; LockDelaySeconds=Unknown"
    exit 0
fi

if ! command -v gsettings >/dev/null 2>&1; then
    echo "Endpoint=$endpoint; ScreenLockEnabled=Unknown; IdleTimeSeconds=Unknown; LockDelaySeconds=Unknown"
    exit 0
fi

uid=$(id -u "$user" 2>/dev/null)

if [ -z "$uid" ]; then
    echo "Endpoint=$endpoint; ScreenLockEnabled=Unknown; IdleTimeSeconds=Unknown; LockDelaySeconds=Unknown"
    exit 0
fi

run_gsettings() {
    timeout 5s sudo -n -u "$user" \
        env DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/${uid}/bus" \
        gsettings "$@" 2>/dev/null
}

# Read GNOME settings
lock_enabled=$(run_gsettings get \
    org.gnome.desktop.screensaver lock-enabled)

idle_raw=$(run_gsettings get \
    org.gnome.desktop.session idle-delay)

lock_raw=$(run_gsettings get \
    org.gnome.desktop.screensaver lock-delay)

# Typical GNOME output:
# uint32 300
#
# Grab the second field, not "32" from uint32.
idle_seconds=$(echo "$idle_raw" | awk '{print $2}')
lock_seconds=$(echo "$lock_raw" | awk '{print $2}')

# Validate values
if ! [[ "$idle_seconds" =~ ^[0-9]+$ ]]; then
    idle_seconds="Unknown"
fi

if ! [[ "$lock_seconds" =~ ^[0-9]+$ ]]; then
    lock_seconds="Unknown"
fi

# Determine whether automatic locking is configured
if [ "$lock_enabled" = "true" ] && \
   [ "$idle_seconds" != "Unknown" ] && \
   [ "$idle_seconds" -gt 0 ]; then

    enabled="Yes"

elif [ "$lock_enabled" = "false" ] || \
     { [ "$idle_seconds" != "Unknown" ] && [ "$idle_seconds" -eq 0 ]; }; then

    enabled="No"

else
    enabled="Unknown"
fi

echo "Endpoint=$endpoint; ScreenLockEnabled=$enabled; IdleTimeSeconds=$idle_seconds; LockDelaySeconds=$lock_seconds"

exit 0