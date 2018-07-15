#-*-coding:utf8-*-
import sys, os, commands, platform, glob
from bs4 import *
import chardet, pdb
from peel_xml import *
# 9/10: list up entries, list up all kinds of tags
# 9/12: list up the necessary tags for lexicon. design mysql table structure.
# 9/21: parse to be with tag, attrib, text


cur_os = platform.system()
#g_orth_count = 0

def get_from_sub_dir(d, entries_f, par_d=''):
	outfile = entries_f
	#ofile = open('tags.' + d, 'w')
	#entries_f.write('%s\n' %(par_d + d))
	os.chdir(d)
	outfile.write('\n+++%s-%s+++' %(par_d, d))
	files = glob.glob('*.xml')
	f_n = 0
	if par_d != '' : par_d += '_'
	for f in files :
		f_n += 1
		#entries_f.write('%s:%d:%s\n' %(par_d + d, f_n, f.replace('.xml', '')))
		f_o = f + '.unxml'
		#parse_xml(f, f_o)
		peel_file(f, outfile)
		#get_tags (f, ofile)
	os.chdir('..')
	#ofile.close()


def batch_proc(in_dir):
	entries_f = open('sdic_all.data', 'w')
	os.chdir(in_dir)
	print os.getcwd()
	dirs = glob.glob('*')
	#entries_f = open('all.entries', 'w')
	#  02.verb, 12.root, 15.frozen have sub dirs.
	# 17.special has just one file which has many entries.
	for d in dirs :
		print d
		if d.startswith('02.') or d.startswith('12.') or d.startswith('15.'):
			os.chdir(d)
			subdirs = glob.glob('*')
			for subd in subdirs :
				print subd
				get_from_sub_dir(subd, entries_f, d)
			os.chdir('..')

		elif d.startswith('17.'):
			get_from_dir(d, entries_f)
		else:
			get_from_sub_dir(d, entries_f)

	entries_f.close()
	os.chdir('..')
	print 'show this file :%s' %(entries_f.name)

def get_tags(infn, of):
	soup = BeautifulSoup(open(infn), "xml")
	for tag in soup.find_all(True):
		of.write('%s\n' %tag.name) #.encode('utf8'))

def get_from_dir(d, entries_f):
	outfile = entries_f
	#ofile = open('tags.' + d, 'w')
	#entries_f.write('%s\n' %d)
	outfile.write('\n+++%s+++' %d)
	os.chdir(d)
	files = glob.glob('*.xml')
	for f in files :
		print f
		#f_o = f + '.unxml'
		peel_file(f, outfile)
	os.chdir('..')
	#ofile.close()

	return

def parse_xml(infn, outfn):
	of = open(outfn, 'w')
	soup = BeautifulSoup(open(infn), "xml")
	#of.write('%s' %(soup.get_text()))
	#for tag in soup.find_all(True):
	#	of.write('%s\n' %tag.name) #.encode('utf8'))
	str_out = soup.get_text().encode('utf8') #beautifulsoup detects input document's encoding and converts into Unicode. So, it needs to encode based on your system encoding. it's character ☃ . :-)
	of.write('%s' %str_out)
	of.close()
	return 0


def fn_decode(instr):
	if cur_os != "Windows":
		tab = instr.split('/')
		for par in tab :
			print chardet.detect(par)['encoding']

if __name__ == "__main__":
	try :
		#pdb.set_trace()
		from datetime import * #timedelta
		now = datetime.now()
		if cur_os != "Windows": #sejong directory
			#print chardet.detect(sys.argv[1])['encoding']
			#print commands.getstatus("sudo rm -r '%s/tags.*'" %(sys.argv[1]))
			#print commands.getstatus("sudo rm -r 'sdic/*/tags.*'")
			batch_proc(sys.argv[1]) #parse_xml(infn, sys.argv[1])
		then = datetime.now()
		tdelta = now - then
		print 'spent time(seconds)', tdelta.total_seconds()
	except Exception, e:
		print e
