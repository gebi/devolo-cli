#!/usr/bin/env python3

import requests
import click

# global options
DEBUG=None
DRYRUN=None

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def getData(devolo_host):
    r = requests.get(f"http://{devolo_host}/assets/data.cfl")
    if r.status_code == 200:
        return parseData(r)
    else:
        raise RuntimeError(f"Http response Code: {r.status_code}")

def parseData(asset_data_request):
    asset_data = {}
    for line in asset_data_request.iter_lines():
        if line:
            (k,v) = line.split(b'=', 1)
            assert(not k in asset_data)
            asset_data[k.decode('utf-8')] = v.decode('utf-8')
    return asset_data

def printData(asset_data):
    for (k,v) in asset_data.items():
        print(f"{k}={v}")

def sendReboot(devolo_host, csrf_token):
    data = {
        'SYSTEM.GENERAL.HW_RESET': '1',
        '.CSRFTOKEN': csrf_token,
    }
    return requests.post(f'http://{devolo_host}/', data=data, verify=False)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug/--no-debug', default=False, help="Print output of all cmds used")
@click.option("--dry-run", default=False, is_flag=True, help="Just output cmds used to get mp4 packet info")
def cli(debug, dry_run):
    global DEBUG
    DEBUG=debug
    global DRYRUN
    DRYRUN=dry_run

@cli.command()
@click.argument("devolo_ip")
def data(devolo_ip):
    """Get asset data of devolo powerlan adapter"""
    asset_data = getData(devolo_ip)
    printData(asset_data)

@cli.command()
@click.argument("devolo_ip")
def reboot(devolo_ip):
    """Reboot devolo powerlan adapter"""
    asset_data = getData(devolo_ip)
    csrf_token = asset_data['CSRFTOKEN']
    # FIXME - check uptime before and after to check for proper reboot?
    r = sendReboot(devolo_ip, csrf_token)
    print(r)

@cli.command()
@click.argument("devolo_ip")
@click.argument("syslog_dest_ip")
@click.option("--port", default=20113, type=int, help="Remote syslog port")
def syslog(devolo_ip, syslog_dest_ip, port):
    """EXPERIMENTAL: enable syslog on device, does not yet work, returns 403"""
    asset_data = getData(devolo_ip)
    csrf_token = asset_data['CSRFTOKEN']
    data = {
        'SYSLOG.GENERAL.ENABLE': 'YES',
        'SYSLOG.OUTPUT.IP': syslog_dest_ip,
        'SYSLOG.OUTPUT.PORT': port,
        'SYSLOG.OUTPUT.MODE': 'udp',
        'SYSLOG.GENERAL.OUTPUT_REDIRECTION:': 'mandangastyle',
        '.CSRFTOKEN': csrf_token,
    }
    r = requests.post(f'http://{devolo_ip}/customization/rsyslog', data=data, verify=False)
    print(r)


if __name__ == "__main__":
    cli()
