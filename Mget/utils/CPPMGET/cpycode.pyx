
cimport cpycode

cdef cpycode.Common * common = new cpycode.Common()
cdef cpycode.MGet * mget = new cpycode.MGet()

cdef class MGet:
	@staticmethod
	def write_string (const char *s): common.report(s)

	@staticmethod
	def _time(): return common.get_time()

	@staticmethod
	def get_time(): return MGet._time().decode()

	@staticmethod
	def _error(cpycode.string msg = "", short status = 0): mget.print_error(msg, status)

	def init_(self, url = None, **kwargs):
		site = kwargs.pop('site', None)
		cur_dl = kwargs.pop('cdl', None)
		tot_dl = kwargs.pop('tot', None)
		wpage = kwargs.pop('wpage', False)
		epage = kwargs.pop('epage', False)

		if wpage or epage: string = "[%s] [%s] (Downloading webpage %s:%s)" % (self.get_time(), site, cur_dl, tot_dl)
		elif url: string = "[Mget Info] Location: %s" % (url)
		else: string = "[%s] [%s] (Download %s:%s)" % (self.get_time(), site, cur_dl, tot_dl)

		MGet.write_string(string.encode())

	def get_term_width(self): return common.get_term_width()
	def progress(self, float cursize, float total): return mget.get_progress(cursize, total, False)
	def get_progress(self, float cursize, float total): return mget.get_progress(cursize, total, True)
	def get_expected(self, float total, float percent): return mget.get_expected(total, percent)

	def trying(self, int trying, int cursize, int filesize):
		mget.print_trying(trying, cursize, filesize)

	def best_block_size(self, float est_time, float bytes):
		return mget.best_block_size(est_time, bytes)

	def format_size(self, float byte): return mget.format_bytes(byte).decode()
	def calc_speed (self, float dif, float bytes): return mget.calc_speed(dif, bytes)
	def calc_eta(self, float dif, float bytes, float current, float total): 
		return mget.calc_eta(dif, bytes, current, total)

	def quitting(self, cpycode.string filename, float cursize, float filesize):
		mget.quitting(filename, int(cursize), int(filesize))

	def done_dl(self, cpycode.string speed = "", cpycode.string filename = "", int cursize = 0, int filesize = 0):
		mget.done_dl(speed, filename, cursize, filesize)

	def done_multi_dl(self, int total, int done): mget.done_multi_dl(total, done)

	def print_info(self, info = {}):
		cdef cpycode.m_dict dic

		dic["filesize"].m_int	 = info["filesize"]
		dic["cursize"].m_int 	 = info["cursize"]
		dic["expected"].m_int 	 = info["expected"]
		dic["status"].m_int 	 = info["status"]
		dic["quit_size"].m_float = info["quit_size"]
		dic["resuming"].m_bool 	 = info["resuming"]
		dic["quiet_mode"].m_bool = info["quiet_mode"]
		dic["dump_info"].m_bool  = info["dump_info"]
		dic["filename"].m_str 	 = info["filename"].encode()
		dic["type"].m_str 	 = info["type"].encode()
		dic["proxy"].m_str 	 = info["proxy"].encode()

		mget.print_info(dic)

del mget
del common
