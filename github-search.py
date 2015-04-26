import sys
import signal
import string
import urllib

from lxml import html


def printHelp():
	print "GitHub-Search 1.0 by cecco4"
	print "\tprovide github repo links\n" 	
	print "use: github-search <name_to_search> [OPTIONS]"
	print "\noptions:"
	print "\t-n NUM\tnumber of pages to output (a page contains 10 repo); default is \"-n 1\"" 
	print "\t-u\tsearch by user and for each user provide a list of his repositories"
	print "\t-h\tprint this message\n" 

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


#print 'Argument List:', str(sys.argv)
class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



#Repo Search
def RepoSearch(url):
	if url is None: repeat= True 
	else: repeat=False

	for np in range(1,maxpg+1):
		if repeat: 
			url = "https://github.com/search?p="+ str(np) +"&q="+search+"&type=Repositories"
		else:
			if np >1: return			
		page = html.fromstring(urllib.urlopen(url).read())

		if len(page.find_class('repo-list-name')) ==0:
			tmp = "Too many requests"
			if urllib.urlopen(url).read().find(tmp) != -1:
				print col.FAIL, col.BOLD,"Due to GitHub policy you can't make too many request, wait a minute!",col.ENDC
				break

			if np==1:
				print col.FAIL, col.BOLD,"Repo not found", col.ENDC
			break

		for link in page.find_class('repo-list-name'):
			rep = link.getchildren()[0].get('href')
			print rep,":"
			print col.OKBLUE,col.BOLD, "\thttps://github.com"+rep+".git\n", col.ENDC
	return



def UserSearch():
	for np in range(1,maxpg+1):
		url = "https://github.com/search?p="+ str(np) +"&q="+search+"&type=Users"			
		page = html.fromstring(urllib.urlopen(url).read())

		if len(page.find_class('user-list-info')) ==0:
			tmp = "Too many requests"
			if urllib.urlopen(url).read().find(tmp) != -1:
				print col.FAIL, col.BOLD,"Due to GitHub policy you can't make too many request, wait a minute!",col.ENDC
				break

			if np==1:
				print col.FAIL, col.BOLD,"Repo not found", col.ENDC
			break

		for link in page.find_class('user-list-info'):
			usr = link.getchildren()[0].get('href')
			print col.OKGREEN, col.BOLD,usr[1:],":",col.ENDC
			RepoSearch("https://github.com"+usr+"?tab=repositories")
			print "\n"
	return



maxpg=1


narg =len(sys.argv);
if(narg == 1):
	print '\tno arguments! "-h" for help'
	sys.exit()


User = False
search= None
i=1
while i<narg:
	if sys.argv[i] == "-n":
		if i+1<narg and sys.argv[i+1].isdigit():
			maxpg = string.atoi(sys.argv[i+1])
			i=i+2
			continue
		else:
			print "\t-n require a number argument"
			sys.exit()
	elif sys.argv[i] == "-u":
		User = True
	elif sys.argv[i] == "-h":
		printHelp()
		sys.exit()
	elif sys.argv[i][0] == "-":
		print "\tno argument called "+ sys.argv[i]
		sys.exit()
	else:
		if search == None:
			if sys.argv[i][0] == "\"":
				search = sys.argv[i][1:len(sys.argv[i])]
			else:
				search = sys.argv[i]
		else:
			print "\ttoo much names to search"
			sys.exit()
	i = i+1
	

if search ==None:
	print "\tno Repo to search"
	sys.exit()
else:
	print col.OKGREEN, col.BOLD,"\tSearching for "+search, col.ENDC


if User== False:
	RepoSearch(None)
else:
	UserSearch()








