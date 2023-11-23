# Mac - Power Management Settings


`pmset` 命令

* pmset -g sched: See the current schedule.
* sudo pmset repeat wake M 8:00:00: Schedule your Mac to wake at 8:00 a.m. every Monday.
* sudo pmset repeat cancel: Cancel the current schedule.

`man pmset`:

[Schedule your Mac to turn on or off in Terminal](https://support.apple.com/guide/mac-help/schedule-your-mac-to-turn-on-or-off-mchl40376151/13.0/mac/13.0)

[Power Management & Scheduling via Command Line](https://www.macos.utah.edu/documentation/administration/pmset.html)

### Settings
displaysleep - display sleep timer; replaces 'dim' argument in 10.4
     (value in minutes, or 0 to disable)
     
     disksleep - disk spindown timer; replaces 'spindown' argument in 10.4
     (value in minutes, or 0 to disable)
     
     sleep - system sleep timer (value in minutes, or 0 to disable)
     
     womp - wake on ethernet magic packet (value = 0/1). Same as "Wake for
     network access" in System Settings.
     
     ring - wake on modem ring (value = 0/1)
     powernap - enable/disable Power Nap on supported machines (value = 0/1)
     
     proximitywake - On supported systems, this option controls system wake
     from sleep based on proximity of devices using same iCloud id. (value =
     0/1)
     
     autorestart - automatic restart on power loss (value = 0/1)
     
     lidwake - wake the machine when the laptop lid (or clamshell) is opened
     (value = 0/1)
     
     acwake - wake the machine when power source (AC/battery) is changed
     (value = 0/1)

lessbright - slightly turn down display brightness when switching to this
     power source (value = 0/1)
     
     halfdim - display sleep will use an intermediate half-brightness state
     between full brightness and fully off  (value = 0/1)
     
     sms - use Sudden Motion Sensor to park disk heads on sudden changes in G
     force (value = 0/1)
     
     hibernatemode - change hibernation mode. Please use caution. (value =
     integer)
     
     hibernatefile - change hibernation image file location. Image may only be
     located on the root volume. Please use caution. (value = path)
     
     ttyskeepawake - prevent idle system sleep when any tty (e.g. remote login
     session) is 'active'. A tty is 'inactive' only when its idle time exceeds
     the system sleep timer. (value = 0/1)
     
     networkoversleep - this setting affects how OS X networking presents
     shared network services during system sleep. This setting is not used by
     all platforms; changing its value is unsupported.
     
     destroyfvkeyonstandby - Destroy File Vault Key when going to standby
     mode. By default File vault keys are retained even when system goes to
     standby. If the keys are destroyed, user will be prompted to enter the
     password while coming out of standby mode.(value: 1 - Destroy, 0 -
     Retain)
     
### SCHEDULED EVENT ARGUMENTS

     type - one of sleep, wake, poweron, shutdown, wakeorpoweron
     
     date/time - "MM/dd/yy HH:mm:ss" (in 24 hour format; must be in quotes)
     
     time - HH:mm:ss
     
     weekdays - a subset of MTWRFSU ("M" and "MTWRF" are valid strings)
     
     owner - a string describing the person or program who is scheduling this
     
     one-time power event (optional)
     
     
### EXAMPLES

This command sets displaysleep to a 5 minute timer on battery power,
     leaving other settings on battery power and other power sources
     unperturbed.

     pmset -b displaysleep 5

     Sets displaysleep to 10, disksleep to 10, system sleep to 30, and turns
     on WakeOnMagicPacket for ALL power sources (AC, Battery, and UPS) as
     appropriate

     pmset -a displaysleep 10 disksleep 10 sleep 30 womp 1

     For a system with an attached and supported UPS, this instructs the
     system to perform an emergency shutdown when UPS battery drains to below
     40%.

     pmset -u haltlevel 40

     For a system with an attached and supported UPS, this instructs the
     system to perform an emergency shutdown when UPS battery drains to below
     25%, or when the UPS estimates it has less than 30 minutes remaining
     runtime. The system shuts down as soon as either of these conditions is
     met.

     pmset -u haltlevel 25 haltremain 30

     For a system with an attached and supported UPS, this instructs the
     system to perform an emergency shutdown after 2 minutes of running on UPS
     battery power.

     pmset -u haltafter 2

     Schedules the system to automatically wake from sleep on July 4, 2016, at
     8PM.

     pmset schedule wake "07/04/16 20:00:00"

     Schedules a repeating shutdown to occur each day, Tuesday through
     Saturday, at 11AM.

     pmset repeat shutdown TWRFS 11:00:00

     Schedules a repeating wake or power on event every tuesday at 12:00 noon,
     and a repeating sleep event every night at 8:00 PM.

     pmset repeat wakeorpoweron T 12:00:00 sleep MTWRFSU 20:00:00

     Cancels all scheduled system sleep, shutdown, wake, and power on events.

     pmset repeat cancel

     Prints the power management settings in use by the system.
     pmset -g

     Prints a snapshot of battery/power source state at the moment.

     pmset -g batt

     If your system suddenly sleeps on battery power with 20-50% of capacity
     remaining, leave this command running in a Terminal window. When you see
     the problem and later power and wake the computer, you'll be able to
     detect sudden discontinuities (like a jump from 30% to 0%) indicative of
     an aging battery.

     pmset -g pslog
     
 
### FILES

     All changes made through pmset are saved in a persistent preferences file
     (per-system, not per-user) at
     /Library/Preferences/SystemConfiguration/com.apple.PowerManagement.plist

     Scheduled power on/off events are stored separately in
     /Library/Preferences/SystemConfiguration/com.apple.AutoWake.plist

     pmset modifies the same file that System Settings modifies.
     
