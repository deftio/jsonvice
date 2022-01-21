#!/usr/bin/env python3

import pkg_resources  # part of setuptools
version = pkg_resources.require("jsonvice")[0].version

"""
	jsonvice utility version: """ + version + """"
	* remove spaces/tabs
	* optionally trims floating point numerical precision
	__doc__
"""

"""
	@copy Copyright (C) <2021>  <M. A. Chatterjee>
	
	@author M A Chatterjee, deftio [at] deftio [dot] com
	
	-- full license below (BSD 2 clause)-- 
	Copyright (c) 2011-2021, M. A. Chatterjee <deftio at deftio dot com>
	All rights reserved.

	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:

	* Redistributions of source code must retain the above copyright notice, this
	  list of conditions and the following disclaimer.

	* Redistributions in binary form must reproduce the above copyright notice,
	  this list of conditions and the following disclaimer in the documentation
	  and/or other materials provided with the distribution.

	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
	AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
	IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
	FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
	DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
	SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
	CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
	OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

	-- end license --
"""


import json, sys, argparse
from os import truncate
from math import ceil, trunc

from logging import PercentStyle


def cli(cli_args = None):
	"""Process command line arguments."""
	if not cli_args :
		cli_args  = sys.argv[1:]    
	
	parser = argparse.ArgumentParser(description="jsonvice version: "+version+" a json minifier with precision truncation. See examples for info.\n")
	
	parser.add_argument("-p","--prec", help="set output quantization in decimal digits", type=int)
	parser.add_argument("-q","--qtype", help="quant method: round(default), floor, ceil", type=str, default= "round")
	parser.add_argument("-i","--input_file",help="input_file_name (use - stdin)", type=str, default=None)
	parser.add_argument("-o","--output_file",help="output_file_name (use - stdout)", type=str, default=None)
	parser.add_argument("-s","--stats", help="show stats (note output file cannot be stdout)",type=bool, default=True )
	parser.add_argument("-b","--beautify",help="beautify (pretty print) instead of minify, default is off.",action="store_true")
	parser.add_argument("-e","--examples", help="print examples",action="store_true")
	parser.add_argument("-v","--version", help="print version",action="store_true")
	parser.add_argument("--about", help="print about",action="store_true")
	# parser.add_argument("--err_file",help="error_output (default is None)",type=str,default=None)

	args = parser.parse_args(cli_args)

	if (args.examples):
		print (	
		"""
jsonvice """+version+""" examples:

Example1 (minify json with 3 digit floating point using rounding quantization):
jsonvice -i jsoninput.json -o minifiedjson.json -p 3 -q round 

Example2 use stdin and std out 
cat simple_test.json | jsonvice.py -i - -o - > output_test.json

Example3 pretty print
jsonvice -i myfile.json -o output.json -p 3 -b
		""")
		exit()


	if (args.version):
		print ("jsonvice "+version+"\n")
		exit()

	if (args.about):
		print("(c) 2021 M A Chatterjee\nThis program is open source under the BSD-2 LICENSE\nsee https://github.com/deftio/jsonvice\n")
		exit()

	#app globals
	# these are put here so in the future if we could load the config from a file if we extended the program
	appvars = {
		# parameters
		"print_stats" : True,
		"prec" : None,
		"qtype" : "round",
		"instream_name": None,
		"outstream_name" : None,
		"beautify" : False,

		# internal state vars
		"fin"  : None,  	#input file stream handle
		"fout" : None,		#output file stream handle
		"indata" : "",      #input buffer
		"outdata" : ""	    #output buffer
	}

	#update from cli etc
	appvars["prec"]  = args.prec
	appvars["qtype"] = args.qtype
	appvars["print_stats"] = args.stats
	appvars["beautify"] = args.beautify
	
	# i/o == get our stream handles
	if args.input_file:
		appvars["instream_name"] = args.input_file
		if args.input_file == '-':
			appvars["fin"] = sys.stdin
		else:
			appvars["fin"] = open(args.input_file)
		appvars["indata"] = appvars["fin"].read()  
	else:
		print("jsonvice "+str(version)+"\n")
		print ("No input specified.\nType jsonvice --help for options.\n")
		exit()

	if args.output_file:
		appvars["outstream_name"] = args.output_file
		if args.output_file == '-':
			appvars["fout"] = sys.stdout
			appvars["print_stats"] = False # can't print out stats to std out
		else:
			appvars["fout"] = open(args.output_file , "w+")

	#end of processing cli / input config

	# process the data
	appvars["outdata"] = process_data(appvars["indata"], appvars["prec"], appvars["qtype"],appvars["beautify"])

	# write to output stream
	if appvars["fout"] != None:
		appvars["fout"].write(appvars["outdata"])

	#stats
	stats = {
		"input_size"  : len(appvars["indata"]),
		"output_size" : len(appvars["outdata"]),
		"ratio"       : "not-computed"
	}

	stats["output_size"] = len(appvars["outdata"])
	if (stats["input_size"]>0):
		stats["ratio"] = stats["output_size"] / stats["input_size"]

	stats["diff"]      = stats["output_size"] - stats["input_size"]


	if appvars["print_stats"]:
		print("json minifier      :  prec = %s, quant_type: %s" % (str(appvars["prec"]), appvars["qtype"]))
		print("Processed: %s ==> %s " % (appvars["instream_name"], appvars["outstream_name"]))
		print("input  file (bytes): %12d" % stats["input_size"])
		print("output file (bytes): %12d" % stats["output_size"])
		print("diff (bytes) %d,  ratio %1.4f, " %(stats["diff"], stats["ratio"]) )
	

def quant(prec, qtype="round"):  # returns a function which truncates numbers at the specified pirec
	def qx (n):
		if qtype == "trunc" or qtype == "floor":  
			return trunc((float(n)*(10**prec)))/(10**prec) # could use decimal.quantize 

		if qtype == "ceil":
			return ceil((float(n)*(10**prec)))/(10**prec) # could use decimal.quantize 

		return round((float(n)*(10**prec)))/(10**prec)
	return qx

def process_data (injson_stream,  prec=None, qtype="round",beautify=False):  #process json streams to specified prec
	try:
		 
		if (prec):
			rawobj = json.loads(injson_stream,parse_float=quant(prec,qtype))
		else:
			rawobj = json.loads(injson_stream)
		
		if (beautify):
			outjson_stream = json.dumps(rawobj, indent=4, sort_keys=True) +"\n"
		else:
			outjson_stream = json.dumps(rawobj,separators=(',', ":")) 

		return outjson_stream
	except:
		print("error processing input data")
		exit(-1)

if __name__ == "__main__":
	cli()

