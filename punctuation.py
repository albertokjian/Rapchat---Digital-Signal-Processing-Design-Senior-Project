import sys

if __name__=="__main__":
	# Usage: python punctuation.py "file_name.txt" "output.txt"
	if len(sys.argv) < 2:
		print('usage: %s [input_filename] [output_filename]' % sys.argv[0])
		sys.exit(1)
	filename = sys.argv[1]
	if len(sys.argv) == 3:
		output = sys.argv[2]
    
	# Parse speech file for individual sentence
	# fragments and store in transcript list
	transcript = []
	# list containing punctuations to split by
	punctuations = [',', '.', '-', '?', ';', '!']
	with open(filename) as f:
		for line in f:
			fragment = []
			for char in line:
				if char not in punctuations:
					if fragment or char != ' ':
						fragment.append(char)
				else:
					transcript.append("".join(fragment))
					fragment = []

	for line in transcript:
		print(line)			

if len(sys.argv) == 3:
	with open(output, 'w') as f:
		for item in transcript:
			f.write("%s\n" % item)