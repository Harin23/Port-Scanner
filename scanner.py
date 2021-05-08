import socket
import common_ports as cp
import re

def get_open_ports(target, port_range, verbose=False):
  if re.match("[a-z]+", target, re.I) != None:
    try:
      ip = socket.gethostbyname(target)
    except socket.gaierror:
      return "Error: Invalid hostname"
  else:
    try:
      ip = socket.gethostbyname(target)
    except socket.gaierror:
      return "Error: Invalid IP address"

  open_ports = []
  for key in cp.ports_and_services:
    if key >= port_range[0] and key <= port_range[-1]:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(5)
      if s.connect_ex((ip, key)) == 0:
        open_ports.append(key)
      s.close()
  
  if verbose == False:
    print(open_ports)
  else:
    try:
      hostname = socket.gethostbyaddr(ip)[0]
      header = 'Open ports for %s (%s)'%(hostname, ip)+'\nPORT     SERVICE'
    except socket.herror:
      header = 'Open ports for %s'%ip+'\nPORT     SERVICE'
    for port in open_ports:
      service = cp.ports_and_services[port]
      numberOfSpaces = len('PORT     ') - len(str(port))
      header += '\n'+ str(port) + numberOfSpaces*' '+service
    print(header)
