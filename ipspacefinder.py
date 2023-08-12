import argparse
import ipaddress
import math

parser = argparse.ArgumentParser(
                    prog='ipspacefinder',
                    description='Given an IPv4 network and list of subnets, identify the minimum unused subnets within that network space. ' +
                    'This program might be useful for system administrators trying to identify unused IP space within their network.',
                    formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=40))
parser.add_argument('-n','--network', required=True, help='An IPv4 network address in CIDR notation.')
parser.add_argument('-f','--file', required=True, help = 'A text file containing a list of CIDR notated IPv4 subnet addresses ' +
                         'within the parent network. Each subnet should be separated by a newline.')
parser.add_argument('-a', '--all', action='store_true', 
                    help='Return both input and output subnets. If this flag is not set, only the output subnets will be returned.')
args = parser.parse_args()

"""
Return a list of sorted, unique ipaddress.ip_network objects within the scope of the input network. 
"""
def load_subnets(network, subnets_file):
    # TODO: Find a few to do this in lines. 
    subnets_sorted = sorted([ipaddress.ip_network(subnet.rstrip()) for subnet in subnets_file])
    subnets_unique = []
    for subnet in subnets_sorted:
        if network.overlaps(subnet):
            subnets_unique.append(subnet)
    return subnets_unique

"""
Return the """
def get_largest_mask(network_address, next_subnet, delta):
    # TODO: Find a more efficient way of determing largest legal subnet mask that does not overlap with next subnet. 
    log2_delta = math.log(delta, 2)
    if log2_delta % 2 == 0:
        return int(32 - log2_delta)
    
    for i in range(1, 33):
        try:
            if not ipaddress.ip_network(str(network_address)+'/{}'.format(i)).overlaps(next_subnet):
                return i
        except:
            continue
    return 32

def get_available_subnets(network, current_subnets):

    # Add next address network after input network as the upper bound of loop. 
    upper_bound = ipaddress.ip_network(int(network.broadcast_address+1))
    current_subnets.append(upper_bound)

    available_subnets = []
    i = 0

    while i < len(current_subnets) - 1:
    # for i in range(len(current_subnets)-1):

        # Identify number of hosts between current and next subnet.
        # If that number is zero, subnet1 and subnet2 are contiguous and program will 
        # continue to the next comparison. 
        subnet2 = current_subnets[i + 1]
        subnet1 = current_subnets[i]

        # Verify that subnet1 is in scope of input network 
        if not network.overlaps(subnet1):
            i += 1
            continue
            
        # Calculate differnece in host addresses between next subnet's network addr and
        # current subnet's broadcast address. 
        delta = int(subnet2.network_address) - int(subnet1.broadcast_address + 1)

        if delta == 0:
            i +=1 
            continue

        # Network address of next subnet is equal to previous subnet's broadcast address + 1
        new_network_addr = ipaddress.IPv4Address(int(subnet1.broadcast_address + 1))

        # Identify largest subnet to insert between subnet1 and subnet2 that:
        #   1. Has a legal netmask   
        #   2. Does not overlap with subnet2 
        new_network_mask = get_largest_mask(new_network_addr, subnet2, delta)

        # Create IPv4Address object for new subnet and insert at next position in subnet list. 
        new_subnet = ipaddress.ip_network(str(new_network_addr)+'/{}'.format(new_network_mask))        
        available_subnets.append(new_subnet)
        current_subnets.insert(i+1, new_subnet)

        i += 1

    # Remove upper bound 
    current_subnets.remove(upper_bound)

    return available_subnets

if __name__ == '__main__':
    network = ipaddress.ip_network(args.network.rstrip())
    subnets_file = open(args.file)

    # Parse file for list of unique, in-scope IPv4Network objects. 
    current_subnets = load_subnets(network, subnets_file)

    # Get list of available IPv4Network objects. 
    available_subnets = get_available_subnets(network, current_subnets)

    if args.all:
        print("\nMinimum number of subnets in network {}. Available subnets are indented:\n".format(str(network)))
        for subnet in current_subnets:
            if subnet in available_subnets:
                    print("\t"+str(subnet))
            else:
                print(str(subnet))
    else:
        print("\nAvailable subnets in network {}: \n".format(str(network)))
        for subnet in available_subnets:
            print(str(subnet))

