
#ifndef _MGET_COMMON_H__
#define _MGET_COMMON_H__

namespace mget {
const char* format(size_t, const char*, ...);

typedef std::map<std::string, std::string> dict;
typedef std::vector<std::string> list;

template <class> class m_string;
template <> class m_string<char *>: public std::string {
public:
	m_string (const char *s) : std::string(s) { _string = s; };
	list split (char deli = '\n');
	std::string join (list, std::string = "");
	std::string operator* (int );

private:
	std::string _string;
	list _list;
};

class Common {
public:
	Common();

	void report (std::string );
	int get_term_width (void );
	const char * get_time (void );
};

typedef m_string<char*> m_str;
}

#endif /* _MGET_COMMON_H__ */
