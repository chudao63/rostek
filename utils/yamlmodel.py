import yaml, logging

class YamlReadWrite:
	def init_base_path(self, basePath):
		self.filterFile = basePath + "/configure/filter.yaml"
		self.deleteFile = basePath + "/configure/delete.yaml"
		self.patchFile = basePath + "/configure/patch.yaml"
		self.postFile = basePath + "/configure/post.yaml"
		self.tableFile = basePath + "/configure/table.yaml"

	@staticmethod
	def read(fileName):
		"Doc du lieu tu file yaml"
		logging.info(fileName)
		with open(fileName) as file:
			data = yaml.load(file, Loader=yaml.FullLoader)
		return data

	@staticmethod
	def write(fileName, data):
		"Ghi du lieu vao file yaml"
		with open(fileName, 'w+') as file:
			yaml.dump(data, file,  explicit_start=True,sort_keys=False,  allow_unicode=True)

	def get_filter(self):
		"""
		Doc du lieu vao file filter yaml
		"""
		return YamlReadWrite.read(self.filterFile)

	def get_table(self):
		"""
		Doc du lieu vao file filter yaml
		"""
		return YamlReadWrite.read(self.tableFile)

	def get_post(self):
		return YamlReadWrite.read(self.postFile)

	def set_post(self, data):
		return YamlReadWrite.write(self.postFile, data)

	def get_patch(self):
		return YamlReadWrite.read(self.patchFile)

	def set_patch(self, data):
		return YamlReadWrite.write(self.patchFile, data)

	def get_delete(self):
		return YamlReadWrite.read(self.deleteFile)

	def set_delete(self, data):
		return YamlReadWrite.write(self.deleteFile, data)
