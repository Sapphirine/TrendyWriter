# filter an article form html file to find the trending topic
def main():
	path = 'res/'
	file_name = 'Tech and Internet Industry News - HuffPost Tech'
	with open(path+file_name+'.html', 'r') as reading_file:
		print reading_file.readline()
		print reading_file.readline()

if __name__ == '__main__' :
	main()
