"""jc - JSON CLI output utility arp Parser

Usage:
    specify --arp as the first argument if the piped input is coming from arp

Example:

$ arp | jc --arp -p
[
  {
    "address": "gateway",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "flags_mask": "C",
    "iface": "ens33"
  },
  {
    "address": "192.168.71.1",
    "hwtype": "ether",
    "hwaddress": "00:50:56:c0:00:08",
    "flags_mask": "C",
    "iface": "ens33"
  },
  {
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "flags_mask": "C",
    "iface": "ens33"
  }
]

$ arp -a | jc --arp -p
[
  {
    "name": "?",
    "address": "192.168.71.1",
    "hwtype": "ether",
    "hwaddress": "00:50:56:c0:00:08",
    "iface": "ens33"
  },
  {
    "name": "?",
    "address": "192.168.71.254",
    "hwtype": "ether",
    "hwaddress": "00:50:56:fe:7a:b4",
    "iface": "ens33"
  },
  {
    "name": "_gateway",
    "address": "192.168.71.2",
    "hwtype": "ether",
    "hwaddress": "00:50:56:f7:4a:fc",
    "iface": "ens33"
  }
]
"""


def parse(data):

    # code adapted from Conor Heine at:
    # https://gist.github.com/cahna/43a1a3ff4d075bcd71f9d7120037a501

    cleandata = data.splitlines()

    # remove final Entries row if -v was used
    if cleandata[-1].find("Entries:") == 0:
        cleandata.pop(-1)

    # detect if linux or bsd style was used
    if cleandata[0].find('Address') == 0:

        # fix header row to change Flags Mask to flags_mask
        cleandata[0] = cleandata[0].replace('Flags Mask', 'flags_mask')

        headers = [h for h in ' '.join(cleandata[0].lower().strip().split()).split() if h]
        raw_data = map(lambda s: s.strip().split(None, len(headers) - 1), cleandata[1:])

        return [dict(zip(headers, r)) for r in raw_data]

    else:
        output = []
        for line in cleandata:
            line = line.split()
            output_line = {}
            output_line['name'] = line[0]
            output_line['address'] = line[1].lstrip('(').rstrip(')')
            output_line['hwtype'] = line[4].lstrip('[').rstrip(']')
            output_line['hwaddress'] = line[3]
            output_line['iface'] = line[6]
            output.append(output_line)

        return output
