#!/home/thierno/miniconda3/envs/regex_tester/bin/python

# importing required modules 
import argparse 
  
# create a parser object 
parser = argparse.ArgumentParser(description = "An addition program") 
  
# add argument 
parser.add_argument("add",  metavar = "path", type = str,  
                     help = "All the numbers separated by spaces will be added.") 
  
# parse the arguments from standard input 
args = parser.parse_args() 
  
# check if add argument has any input data. 
# If it has, then print sum of the given numbers 
if args.add: 
    print(args.add)
