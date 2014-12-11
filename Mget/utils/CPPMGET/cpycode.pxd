
from libcpp cimport bool
from libcpp.string cimport string
from libcpp.map cimport map
from libcpp.vector cimport vector

cdef extern from "common.h" namespace "mget":

	cppclass Common:
		Common()
		void report (const char *)
		int get_term_width ()
		const char* get_time()

cdef extern from "main.h":
	struct dtypes:
		int m_int
		bool m_bool
		float m_float
		string m_str

	ctypedef map[string, dtypes] m_dict

cdef extern from "main.h" namespace "mget":

	cppclass MGet:
		MGet()
		void print_trying (int, int, int)
		void print_error (string, short)
		void quitting (string, int, int)
		void done_dl (string, string, int, int)
		void done_multi_dl (int, int)
		void print_info (m_dict& )

		int get_expected (float, float)
		int best_block_size (float, float)

		float get_progress (float, float, bool)

		const char *format_bytes (float )
		const char *format_duration (int )
		const char *calc_speed (float, float)
		const char *calc_eta (float, float, float, float)

