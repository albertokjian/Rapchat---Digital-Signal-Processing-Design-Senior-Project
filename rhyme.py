import pronouncing
import sys

# Return words which rhyme with input word
def rhyme(inp):
	return pronouncing.rhymes(inp)

# Check if two words rhyme
def checkRhyme(first_word, second_word):
	return second_word in rhyme(first_word) or first_word == second_word

if __name__=="__main__":
	# Usage: python rhyme.py "file_name.txt"
	if len(sys.argv) < 2:
		print('usage: %s [input_filename] [output_filename]' % sys.argv[0])
		sys.exit(1)
	filename = sys.argv[1]
	if len(sys.argv) == 3:
		output = sys.argv[2]

	# Parse speech file for individual words
	# and store in transcript list
	transcript = []
	with open(filename) as f:
		for line in f:
			word = []
			for char in line:
				if char == ',':
					break
				word.append(char)
			transcript.append("".join(word[6:]))

	# Find rhyme words spaced less than 'max_words' words apart
	# but at least 'min_words' apart
	rhymes = [] # rhyme words
	indices = [] # transcript indices for rhyme words
	max_words = 8 # max length of a rhyme line
	min_words = 3 # min length of a line
	counter, i = min_words-1, min_words-1
	prevword = ""
	while i < len(transcript):
		j = i+min_words
		while j < i+max_words and j < len(transcript):
			# If two words near each other rhyme, add them
			if checkRhyme(transcript[i], transcript[j]):
				rhymes.append(transcript[i])
				rhymes.append(transcript[j])
				prevword = transcript[j]
				indices.append(i)
				indices.append(j)
				i=j
				counter = min_words - 1
				i += min_words - 1
				break
			j+=1			
		counter += 1
		# If line is too long or word rhymes with previous rhyme, add word 
		if counter == max_words or checkRhyme(prevword, transcript[i]): 
			rhymes.append(transcript[i])
			indices.append(i)
			prevword = transcript[i]
			counter = min_words - 1
			i += min_words - 1
		i+=1
	i,j = 0,0

	# Splitting transcript into lines
	lines = [[] for x in range(len(rhymes)+1)]
	for idx in indices:
		while i <= idx:
			lines[j].append(transcript[i])
			i+=1
		j+=1
	# add the last words into a final line
	while i < len(transcript):
		lines[j].append(transcript[i])
		i+=1
	for line in lines:
		print(line)			

if len(sys.argv) == 3:
	with open(output, 'w') as f:
		for item in lines:
			f.write("%s\n" % item)