from flask_restful import Resource
import subprocess
import os,sys
import git
from utils.vntime import VnTimestamp
from urllib.request import urlopen

class UpdateApi(Resource):
	"""URL: /updatesoftware

	"""
	def get(self):
		old_date = get_lasted_time()
		out = excute_cmd(['git', 'pull'])
		if out:
			message = out.decode('utf-8').replace("\n","")
			if message != "Phần mềm được cập nhật thành công.":
				new_date = get_lasted_time()
				message =  f"Cập nhật thành công từ phiên bản {old_date} tới {new_date}"
			return  {"message" : message },200
		else:
			return {"message" : "Không có kết nối mạng" },502

class VersionApi(Resource):
	"""URL: /version

	"""
	def get(self):
		app_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		build_date = get_lasted_time()
		# build_date = "today"
		try:
			f = open( f"{app_path}/app/version.txt", "r")
			version = str(f.read())
		except Exception as e:
			return str(e)
		return {"version" : version, "build_date":build_date },200

def get_lasted_time():
	app_path = os.path.dirname(os.path.realpath(sys.argv[0]))[:-7]
	print(app_path)
	repo = git.Repo(app_path)
	commits = list(repo.iter_commits( max_count=1))
	build_date = commits[0].committed_datetime.strftime("%m/%d/%Y, %H:%M:%S")
	return build_date
	# return "1"

def excute_cmd(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = proc.communicate()
	return out