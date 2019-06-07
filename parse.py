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
			word = []
			for char in line:
				if char == " ":
					transcript.append("".join(word))
					word = []
				elif char in punctuations:
					continue
				else:
					word.append(char)
			transcript.append("".join(word))

if len(sys.argv) == 3:
	with open(output, 'w') as f:
		for item in transcript:
			f.write("%s\n" % item)