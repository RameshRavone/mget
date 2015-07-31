
// MGet Common file..

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <unistd.h>
#include <sys/ioctl.h>

#include <ctime>
#include <cstring>
#include <cstdarg>

#include "common.h"

const char *mget::format (size_t c_size, const char *c_fmt, ...) {
va_list args;
char* buffer = 0;
buffer = new char[c_size];

	va_start(args, c_fmt);
	vsnprintf(buffer, c_size, c_fmt, args);
	va_end(args);

return buffer;
}

mget::Common::Common() { }

void mget::Common::report (std::string str) { std::cout << str << std::endl; }

int mget::Common::get_term_width (void ) {
int cols = 80;
// int lines = 24;

	#ifdef TIOCGSIZE
		struct ttysize ts;
		ioctl(STDIN_FILENO, TIOCGSIZE, &ts);
		cols = ts.ts_cols;
		// lines = ts.ts_lines;

	#elif defined(TIOCGWINSZ)
		struct winsize ts;
		ioctl(STDIN_FILENO, TIOCGWINSZ, &ts);
		cols = ts.ws_col;
		// lines = ts.ws_row;

	#endif /* TIOCGSIZE */

return cols;
}

const char *mget::Common::get_time (void ) {
char *buffer = 0;
buffer = new char[100];

	std::time_t result = std::time(NULL);
	std::strftime(buffer, 100, "%c %Z", std::localtime(&result));

return buffer;
}

mget::list mget::m_string<char*>::split(char delim) {
std::string buf = "";

	for (unsigned int i = 0; i < this->_string.length(); i++) {
		if (this->_string[i] != delim) { buf += this->_string[i]; }
		else if (buf.length() > 0) {
		this->_list.push_back(buf);
		buf = "";
		}
	}
	this->_list.push_back(buf);
	buf = "";

return this->_list;
}

std::string mget::m_string<char*>::join(mget::list array, std::string prefix) {
std::ostringstream oss;

for (unsigned int i = 0; i < array.size(); i++ ) { oss << prefix << array[i] << this->_string; }

return oss.str();
}

std::string mget::m_string<char*>::operator* (int num) {
std::string value = this->_string;

for (int i = 0; i < num; i++ ) { this->_string += value; }

return this->_string;
}
