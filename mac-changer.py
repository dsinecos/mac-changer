#! /usr/bin/env python3

import subprocess
import click
import re


@click.command()
@click.option('--interface', '-i',
              help="Specify the interface for which you'd like to change the MAC address")
@click.option('--mac', '-m',
              help="Specify the new MAC Addr to be assigned to the interface")
def main(interface, mac):
    """
    CLI Tool to change MAC Address of an interface
    """
    current_mac_addr = get_mac_addr(interface)
    print("Current MAC Addr of interface " +
          interface + " - " + current_mac_addr)
    change_mac_addr(interface, mac)
    new_mac_addr = get_mac_addr(interface)
    if(mac == new_mac_addr):
        print("[+] MAC Addr for interface " +
              interface + " changed successfully")
    else:
        print("[-] MAC Addr change for interface " + interface + " failed")


def get_mac_addr(interface):
    ifconfig_result = subprocess.run(
        ["ifconfig", interface], encoding="utf-8", stdout=subprocess.PIPE)
    mac_addr = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",
                         ifconfig_result.stdout)
    if(mac_addr):
        print("[+] MAC Addr of interface " +
              interface + " - " + mac_addr.group(0))
        return mac_addr.group(0)
    else:
        print("[-] MAC Addr of interface " + interface + " not found")
        return None


def change_mac_addr(interface, mac_addr):
    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", mac_addr])
    subprocess.run(["ifconfig", interface, "run"])


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
