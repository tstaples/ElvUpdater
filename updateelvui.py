import os, sys
import urllib2
import zipfile
import tempfile
from distutils.dir_util import copy_tree, remove_tree
from StringIO import StringIO

# TODO: service to check for updates

def copychilddirs(parentdir, dst):
	for childdir in os.listdir(parentdir):
		src = os.path.join(parentdir, childdir)
		dstdir = os.path.join(dst, childdir)
		print("copying %s to %s" % (src, dstdir))
		copy_tree(src, dstdir)


def cleanup(zipbuffer, extracteddir):
	if zipbuffer:
		zipbuffer.close()
	if os.path.isdir(extracteddir):
		remove_tree(extracteddir)


tempdir = tempfile.gettempdir()
addonspath = "C:/Program Files (x86)/World of Warcraft/Interface/AddOns"
#addonspath = "Addons"

elvcore = "ElvUI"
elvconfig = "ElvUI_Config"
extractedroot = ""

url = "http://git.tukui.org/Elv/elvui/repository/archive.zip?ref=master"
data = None
try:
	response = urllib2.urlopen(url)
	data = response.read()
except:
	print("Failed to download data from %s" % url)
	exit(1)

# write the data to a file-like object in memory
buff = StringIO(data)

# extract the core and config dirs from the zip file
try:
	with zipfile.ZipFile(buff, "r") as z:
		namelist = z.namelist()
		toextract = []
		for name in namelist:
			if not ".git" in name:
				toextract.append(name)

		z.extractall(tempdir, toextract)
		extractedroot = os.path.join(tempdir, namelist[0])
except:
	print("Failed to extract contents of zip")
	cleanup(buff, extractedroot)
	exit(1)

# Create a backup
try:
	backupdir = os.path.join(tempdir, "ElvUIBackup")
	copychilddirs(extractedroot, backupdir)
except:
 	print("Failed to create backup; aborting")
 	cleanup(buff, extractedroot)
 	exit(1)

# overwrite the files with the new ones
try:
	copychilddirs(extractedroot, addonspath)
except:
	print("Error copying files to addons dir")
finally:
	cleanup(buff, extractedroot)
