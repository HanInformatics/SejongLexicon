#-*-coding:utf8-*-
import xml.etree.ElementTree as ET
import sys, pdb, chardet


def dict2str(dic):
	outstr = '{'
	for each in dic :
		outstr += each
		outstr += ':'
		outstr += dic[each]
		outstr += ','
	if outstr[-1] ==',' : outstr=outstr[0:-1]
	outstr += '}'
	return outstr

#def print_data(child, outs, depth=''):
def print_data(child, outs, depth=0):
	#pdb.set_trace()
	if child.tag == 'mnt_grp' : return ''
	if child.text == None : return ''
	#print depth, ':', child.tag ,',', child.attrib, ',', child.text
	attrib_str = dict2str(child.attrib)
	out = str(depth) + ':' + child.tag +','+ attrib_str +','+ child.text
	'''
	if child.tag=='orth':
		g_orth_count += 1
		out += '\t' + str(g_orth_count)
	'''
	#print sys.stdout.encoding, type(out)
	#print chardet.detect(outstr)['encoding']
	return outs.append(out.strip())

def peel_file(fn, outfile):

	tree = ET.parse(fn)
	root = tree.getroot()
	str_data =''
	#root = ET.fromstring(str_data)
	#print root.tag
	#print root.attrib

	out = []
	for child in root:
		print_data(child, out, 1)
		for child2 in child:
			if child2.tag == 'mnt_grp' : continue
			print_data(child2, out, 2)
			for child3 in child2:
				if child3.tag == 'mnt_grp' : continue
				print_data(child3, out, 3)
				for child4 in child3:
					if child4.tag == 'mnt_grp' : continue
					print_data(child4, out, 4)
					for child5 in child4:
						if child5.tag == 'mnt_grp' : continue
						print_data(child5, out, 5)
						for child6 in child5:
							if child6.tag == 'mnt_grp' : continue
							print_data(child6, out, 6)
							for child7 in child6:
								if child7.tag == 'mnt_grp' : continue
								print_data(child7, out, 7)
								for child8 in child7:
									if child8.tag == 'mnt_grp' : continue
									print_data(child8, out, 8)
									print 'You should never see this'



	outs = ''
	delim_attr = '\n'
	try:
		for e in out :
			#outs += '\n' + e
			#print '\n' + e
			outfile.write('\n%s' %(e.encode('utf-8')))
		#print 'out', out
		#outfile.write('%s\n' %(outs.encode('utf-8')))
	except Exception, e:
		print e

if __name__ == "__main__":
	outfile = open(sys.argv[2], 'w')
	peel_file(sys.argv[1], outfile)
	outfile.close()
