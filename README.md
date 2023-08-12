# ipspacefinder
Given an IPv4 network and list of subnets, identify unused IP space. 

## Prerequisites

Import requirements:
<code>pip install -r requirements.txt</code>

## Quick Start

1. Identify a network you would like to query for unused subnets. 
2. Create a text file containing a newline-delimited list of subnet addresses in CIDR notation. These network addresses should fall within the supernet you identified in Step 1. For reference, three <i>example</i> input files have been included in this directory.
3. Run <b>ipspacefinder.py</b> to identify the minimum number of subnets in the supernet that do <i>not</i> appear in the input file.


## Sample Input
<code>python3 ipspacefinder.py --network 10.0.0.0/20 --file example-input2.txt --all</code>

The flag <code>--all</code> in the snippet above will output both input and output subnets with the output subnets indented.
