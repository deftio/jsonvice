"""
M A Chatterjee 2021
deftio@deftio.com

Trivial minifier for json removes spaces/tabs, optionally trims of precision.  use --help for help

"""


import json, sys, argparse


parser = argparse.ArgumentParser(description=__doc__)
 
parser.add_argument("-p","--prec", help="set output quantization", type=int)
parser.add_argument("-i","--input_file",help="input_file_name (use - stdin)", type=str, default=None)
parser.add_argument("-o","--output_file",help="output_file_name (use - stdout)", type=str, default=None)
parser.add_argument("--err_file",help="error_output (default is None)",type=str,default=None)
parser.add_argument("-e","--examples", help="print examples",type=bool, default = False  )
#parser.add_argument("-v","--verbose",help="prints stats.  If stdout used for output_file, writes to a file",type=str)

args = parser.parse_args();


if (args.examples):
	print (
	"""
	examples:                                                                                                              \n
	python3 json_prec_minify.py.py < myjsonfiletominify > myoutputfile                                                             
	python3 json_prec_minify.py.py < myjsonfiletominify > myoutputfile -p 5  # saves compact json with float precision of 5 digits 
	python3 -i jsonInput -o minifiedjson -p3                         # uses files, also prints out stats                  
	""")
	exit()

def quant(n):  return round((float(n)*(10**args.prec)))/(10**args.prec) # could use decimal.quantize 

#globals
print_stats = False
fin  = None  	#input file
fout = None		#output file
indata = ""     #input buffer
outdata = ""	#output buffer


# i/o
try:
	if args.input_file:
		if args.input_file == '-':
			fin = sys.stdin
		else:
			fin = open(args.input_file)
		indata = fin.read()  
	else:
		print(__doc__)
		print ("no input specified.")
		exit()

except (e):
	print("error: ", e)
	exit(-1)

if args.output_file:
	if args.output_file == '-':
		fout = sys.stdout
	else:
		fout = open(args.output_file , "w+")
		print_stats = True

#stats
stats = {
	"input_size"  : len(indata),
	"output_size" : len(outdata),
	"ratio"            : "not-computed"
}

if (args.prec):
	outdata = json.dumps(json.loads(indata,parse_float=quant),separators=(',', ":")) 
else:
	outdata = json.dumps(json.loads(indata),separators=(',', ":")) 

stats["output_size"] = len(outdata)
if (stats["input_size"]>0):
	stats["ratio"] = stats["output_size"] / stats["input_size"]

stats["diff"]      = stats["output_size"] - stats["input_size"]

if fout != None:
	fout.write(outdata)

if print_stats:
	print("json minifier      :  prec = %s" % str(args.prec))
	print("input  file (bytes): %12d" % stats["input_size"])
	print("output file (bytes): %12d" % stats["output_size"])
	print("diff (bytes) %d,  ratio %1.4f" %(stats["diff"], stats["ratio"]) )

exit(0)