import os, logging

def check_path(it):
	if it.is_dir():
		if "__" not in it.path:
			return True
	return False

def import_module(module):
	exec(f"from {module} import *")

def add_urls(path):
	urls_path = path+"/urls.py"
	if os.path.isfile(urls_path):
		module = path.replace("/",".") + ".urls"
		module = module.replace("\\",".")
		import_module(module)

def import_all_urls(rootdir):
	"""
	Import all Url 
	"""
	for it in os.scandir(rootdir):
		if check_path(it):
			add_urls(it.path)
			subdir = it.path
			for itSub in os.scandir(subdir):
				if check_path(itSub):
					add_urls(itSub.path)