# %%
from math import log, trunc
import argparse
from fileinput import input

# Instantiate parser
parser = argparse.ArgumentParser(description='Simulating the virtual memory of a CPU cache.')
# Define arguments

# -s cache size in KB
parser.add_argument('-s',   type=int, help='Cache size in KB [1 KB to 8 MB]')
# -b block size in bytes
parser.add_argument('-b',   type=int, help='Block size [4 bytes to 64 bytes]')
# -a associativity
parser.add_argument('-a',   type=int, help='1, 2, 4, 8, or 16')
# -r replacement policy
parser.add_argument('-r',   type=str, help='Replacement policy [RR or RND]')
# -p physical memory in KB
parser.add_argument('-p',   type=int, help='Physical memory in KB [64 KB to 512 GB]')
# -f trace file
#   Not definable in argparse because the assingment requires multiple file inputs. Argparse can do that, but each file needs to have a 
#   -f in front of it and argparse doesn't like that format, instead we use the "other" variable to parse this argument inside of output()

kb_to_byte = lambda kb_val : int(kb_val*1024)
byte_to_kb = lambda byte_val : int(byte_val/1024)


def parse_trace_file(trace_file):
    with input(trace_file) as tfile:
        i = 0
        for line in tfile:
            line_array = line.split(" ")
            # print(line_array)

            if line_array[0] == "EIP":
                address = str(line_array[2])
                read_length = str(line_array[1])[1:3]

                if i<20:
                    print(f"0x{address}: {read_length}")
                    i+=1
                else:
                    return 1
    return 0


def calculate_cache_values(trace_file, cache_size, block_size, associativity, rep_policy, phys_mem):
    # tfile open and read
    # . . .
    address_size = 32
    total_blocks = int(kb_to_byte(cache_size)/block_size)
    offset_size = log(block_size,2)
    index_size = int(log(kb_to_byte(cache_size) / (block_size * associativity),2))
    tag_size = int(address_size - offset_size - index_size)
    # . . .
    total_rows = int(pow(2,index_size))
    overhead_bits = 0
    overhead_size = int(pow(2,block_size) + pow(2,index_size + overhead_bits))
    imp_memory_bytes = int(kb_to_byte(cache_size) + overhead_size)
    imp_memory = int(byte_to_kb(imp_memory_bytes))
    cost = imp_memory*0.15

    return total_blocks, tag_size, index_size, total_rows, overhead_size, imp_memory, imp_memory_bytes, cost


def output(parser):
    # define parser
    #   - Arguments that are defined above go into "args"
    #   - Arguments that are not defined above go into "other"
    #       - If the command line input is corectly formatted, only -f should be in "other"

    args, other = parser.parse_known_args()
    file_list = []

    # parsing through arguments passed through cmd line that were not explicitly defined above
    for i, arg in enumerate(other):
        try:
            # if not "-f" or the value after it, return 0
            if arg == '-f':
                file_list.append(other[i+1])
                last_file = i+1
            elif i != last_file:
                print("Error: incorrect cmd line argument input")
                return 0
        except:
            continue

    print("Cache Simulator - CS 3853 - Instructor Version: 2.02"+"\n")

    for tfile in file_list:
        # output parameters that were input
        print()                                                                              
        print("Trace File:\t"+tfile)
        print()
        print("***** Cache Input Parameters *****")
        print()
        print("Cache Size:\t\t\t\t"+str(args.s)+" KB")
        print("Block Size:\t\t\t\t"+str(args.b)+" bytes")
        print("Associativity:\t\t\t"+str(args.a))
        print("Replacement Policy:\t\t"+args.r)

        # calculate cache values
        total_blocks, tag_size, index_size, total_rows, overhead_size, imp_memory, imp_memory_bytes, cost = calculate_cache_values(tfile, args.s, args.b, args.a, args.r, args.p)
        
        # print calculated values
        print()
        print("***** Cache Calculated Values *****")
        print()
        print("Total Blocks:\t\t\t"+str(total_blocks))
        print("Tag Size:\t\t\t\t"+str(tag_size)+" bits")
        print("Index Size:\t\t\t\t"+str(index_size)+" bits")
        print("Total Rows:\t\t\t\t"+str(total_rows))
        print("Overhead Size:\t\t\t"+str(overhead_size)+" bytes")
        print("Implementation Memory:\t"+str(imp_memory)+" KB ("+str(imp_memory_bytes)+" bytes)")
        print("Cost:\t\t\t\t\t$"+str(round(cost, 2))+"\n")

        # read through trace file
        parse_trace_file(tfile)
    
    return 1

if output(parser) == 0:
    print("fatal error")
    exit()   