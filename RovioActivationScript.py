import os
import sys
import uuid
import re
def get_mac_addresses():
    """
    Retrieves system MAC addresses. 
    Avoids invocation of getmac.exe which may fail or return invalid 
    formatting under standard Wine prefix environments.
    """
    mac_addresses = []
    try:
        mac_int = uuid.getnode()
        if (mac_int >> 40) & 1 == 0:
            formatted_mac = "-".join("{:012X}".format(mac_int)[i:i+2] for i in range(0, 12, 2))
            mac_addresses.append(formatted_mac)
    except Exception:
        pass
    if not mac_addresses:
        try:
            for interface in os.listdir('/sys/class/net/'):
                if interface == 'lo':
                    continue
                with open(f'/sys/class/net/{interface}/address', 'r') as f:
                    mac = f.read().strip().upper().replace(':', '-')
                    if len(mac) == 17:
                        mac_addresses.append(mac)
        except Exception:
            pass
    if not mac_addresses:
        mac_addresses.append("00-00-00-00-00-00")
    return ";".join(list(set(mac_addresses)))
def resolve_wine_locallow_path():
    """
    Resolves the exact LocalLow target path within the active Wine prefix hierarchy.
    """
    wine_prefix = os.environ.get('WINEPREFIX', os.path.expanduser('~/.wine'))
    wine_user = os.environ.get('USER', 'bottle')
    target_path = os.path.join(
        wine_prefix, 
        'drive_c', 
        'users', 
        wine_user, 
        'AppData', 
        'LocalLow', 
        'Rovio', 
        'Bad Piggies'
    )
    return target_path
def main():
    print("Rovio Compatibility Script v1.0.2 [POSIX/WINE Execution Node]\n")
    try:
        hardware_id = get_mac_addresses()
        target_dir = resolve_wine_locallow_path()
        xml_content = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<data>\n'
            '<Boolean key="BDPGS12FL" value="True" />\n'
            '<String key="BDPGS12FL_hardwareID" value="{}" />\n'
            '</data>\n'
        ).format(hardware_id)
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, 'Settings.xml')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        print("Configuration successfully instantiated within the Wine environment.")
        print("Path: {}".format(file_path))
        print("Hardware ID Payload: {}".format(hardware_id))
    except Exception as e:
        print("Execution failure: {}".format(str(e)), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
