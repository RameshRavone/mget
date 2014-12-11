
#ifndef _MGET_MAIN_H__
#define _MGET_MAIN_H__

struct dtypes {
	int m_int;
	float m_float;
	bool m_bool;
	std::string m_str;
};

typedef std::map<std::string, dtypes> m_dict;
typedef std::vector<mget::m_str> m_list;

namespace mget {

class MGet {

public:
	MGet();
	~MGet();
	void print_trying (short, int, int);

	void init_ (std::string, std::string, int, int, bool, bool);
	void print_error (std::string, short);
	void quitting (std::string, int, int);
	void done_dl (std::string, std::string, int, int);
	void done_multi_dl (int, int);
	void print_info (m_dict& );

	int get_expected (float, float);
	int best_block_size (float, float);

	float get_progress (float, float, bool);

	const char *format_bytes (float );
	const char *format_duration (int );
	const char *calc_speed (float, float);
	const char *calc_eta (float, float, float, float);

private:
	struct options_ {
	std::string filename;
	std::string proxy;
	std::string type;
	};

	const char *get_remaining (float, float);
	mget::Common * common;
};

}

#endif /* _MGET_MAIN_H__ */ 
