
// MGet main class file..

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <map>

#include <cstring>
#include <cmath>

#include "common.h"
#include "main.h"

const char* FILE_EXIST = "\nThe file is already fully retrieved; nothing to do.\n";

std::map<int, const char*> responses { {400, "Bad Request"}, {401, "Unauthorized"}, {410, "Gone"},
{403, "Forbidden"}, {404, "Not Found"}, {408, "Request Timeout"}, {300, "Multiple Choices"},
{301, "Moved Permanently"}, {302, "Found"}, {304, "Not Modified"}, {200, "OK"}, {201, "Created"},
{202, "Accepted"}, {204, "No Content"}, {206, "Partial Content"}, {500, "Internal Server Error"},
{501, "Not Implemented"}, {502, "Bad Gateway"}, {503, "Service Unavailable"} };

mget::MGet::MGet () { common = new Common(); }
mget::MGet::~MGet () { delete common; }

void mget::MGet::print_error(std::string m_msg, short m_code = 0) {
	std::string m_error = "System Error";

	if (strlen(m_msg.c_str()) > 0) { m_error = m_msg; }
	if (m_code != 0) { m_error = format(100, "%d %s", m_code,responses[m_code]); }

	const char* result = (m_code == 416) ? FILE_EXIST:format(100, "\nERROR: %s", m_error.c_str());

common->report(result);
}

void mget::MGet::init_ (std::string url, std::string site, int cur_dl, int tot_dl, bool wpage, bool epage) {

	const char *string = "";
	if (wpage or epage) {
	string = format(200, "[%s] [%s] (Downloading webpage %s:%s)", common->get_time(), site.c_str(), cur_dl);
	}
	else if (url.c_str()) {
	string = format(300, "[Mget Info] Location: %s", url.c_str());
	}
	else {
	string = format(150, "[%s] [%s] (Download %s:%s)", common->get_time(), site.c_str(), cur_dl, tot_dl);
	}

common->report(string);
}

void mget::MGet::print_info(m_dict &info) {
	std::string resume = "";
	mget::m_str new_line = "\n";
	mget::list result;

	const char *filename = info["filename"].m_str.c_str();
	const char *proxy = info["proxy"].m_str.c_str();
	const char *type = info["type"].m_str.c_str();

	short status = info["status"].m_int;

	int filesize = info["filesize"].m_int;
	const char *F_filesize = format_bytes(filesize);

	int expected = info["expected"].m_int;
	const char* e_f_size = format_bytes(expected);

	if ( info["quiet_mode"].m_bool ) {
	result.push_back(format(200, "Filesize: %d [%s] -> %s", filesize,F_filesize,filename));

	if (info["quit_size"].m_float != 100.0) {
	resume = (info["resuming"].m_bool) ? get_remaining(info["cursize"].m_int, expected) : "";
	result.push_back(format(150,
			"Expecting to download: %d [%s],%s", expected,e_f_size,resume.c_str()));
	}

	common->report(new_line.join(result, "[MGet Info] "));
	return;
	}
	if (info["quit_size"].m_float == 100.0) {
	resume = (info["resuming"].m_bool) ? get_remaining(info["cursize"].m_int, filesize) : "";
	}

	if (strlen(proxy) > 1) { result.push_back(format(50, "Proxy: %s", proxy)); }

	result.push_back(format(100, "Status code: %d %s", status, responses[status]));
	result.push_back(
		format(200, "Filesize: %d [%s],%s [%s]", filesize,F_filesize,resume.c_str(),type));

	if (info["quit_size"].m_float != 100.0) {
	resume = (info["resuming"].m_bool) ? get_remaining(info["cursize"].m_int,expected) : "";
	result.push_back(
		format(150, "Expecting to download: %d [%s],%s", expected,e_f_size,resume.c_str()));
	}

	if (info["dump_info"].m_bool) { result.push_back(format(200, "Filename: %s", filename)); }
	else { result.push_back(format(200, "Saving to: %s", filename)); }

common->report(new_line.join(result, "[MGet Info] "));
}

void mget::MGet::print_trying (short m_try, int m_csize, int m_tsize) {
	const char* buffer = common->get_time();
	const char* result = format(200,"[%s] Read error at byte [%d/%d] - (try: %d)",
								buffer,m_csize,m_tsize,m_try);

common->report(result);
}

void mget::MGet::quitting(std::string m_fname, int m_csize, int m_tsize) {
	if (m_csize > m_tsize) { m_tsize = m_csize; }
	const char* percent = format(15, "%.1f%%", get_progress(m_csize, m_tsize, true));
	const char* result = format(200, "\n\nQuitting: ‘%s’ at (%s) - [%d/%d]\n",
						m_fname.c_str(),percent,m_csize,m_tsize);
common->report(result);
}

void mget::MGet::done_dl(std::string speed, std::string m_fname, int m_csize, int m_tsize) {
	if (m_csize > m_tsize) { m_tsize = m_csize; }
	const char* percent = format(15, "%.1f%%", get_progress(m_csize, m_tsize, true));
	const char* result = format(200, "\n\n[%s] %s at (%s) - ‘%s’ -> [%d/%d]\n",
		common->get_time(),percent,speed.c_str(),m_fname.c_str(),m_csize,m_tsize);

common->report(result);
}

void mget::MGet::done_multi_dl(int m_tot_dl, int m_tot_done) {
	const char* result = format(200, "[%s] - ‘%d:%d’ files downloaded from mangafox.\n",
							common->get_time(),m_tot_done,m_tot_dl);

common->report(result);
}

int mget::MGet::get_expected (float m_tsize, float percent) { return (m_tsize * percent / 100.0); }
int mget::MGet::best_block_size (float m_est_time, float bytes) {
	float new_min = std::max(bytes / 2.0, 1.0);
	float new_max = std::min(std::max(bytes * 2.0, 1.0), 4194304.0);

	if (m_est_time < 0.001) { return int(new_max); }

	float rate = bytes / m_est_time;

	if (rate > new_max) { return new_max; }
	if (rate < new_min) { return new_min; }

return rate;
}

float mget::MGet::get_progress (float m_csize, float m_tsize, bool m_percent = false) {
	float progress = m_csize / m_tsize;
	if (progress < 0) { progress = 0; }
	if (progress > 1) { progress = 1; }

	if ( m_percent ) return progress * 100.0;

return progress;
}

const char* mget::MGet::get_remaining(float m_csize, float m_tsize) {
	if (m_csize > m_tsize) { return " 0 [UNKNOWN] remaining"; }
	int B_size = m_tsize - m_csize;
	const char* F_size = format_bytes(B_size);

return format(50, " %d [%s] remaining", B_size, F_size);
}

const char* mget::MGet::format_bytes(float bytes){
	char UNITS[] = {'B', 'K', 'M', 'G'};

	if ( bytes > 1 ) {
	int exponent = std::log(bytes) / std::log(1024.0);
	float quotient = bytes / std::pow(1024, exponent);
	char unit =  UNITS[exponent];

	return format(10, (unit == 'B') ? "%.f%c" : "%.2f%c", quotient, unit);
	}

return "Unknown";
}

const char* mget::MGet::format_duration(int duration = 0) {
	int mins = (duration / 60);
	int secs = (duration % 60);
	int hours = (mins / 60);
	mins = (mins % 60);

	if ( hours > 99 ) { return "--:--"; }
	else if ( hours == 0 && mins == 0 ) { return format(10, "    %02ds", secs); }
	else if ( hours == 0) { return format(10, "%02dm %02ds", mins, secs); }
	else { return format(10, "%02dh %02dm", hours, mins); }
}

const char* mget::MGet::calc_speed (float dif, float bytes) {
	if (bytes == 0 or dif < 0.001) { return format(10, "%6s", "--.-K/s"); }

return format(10, "%s/s", format_bytes(bytes / dif));
}

const char* mget::MGet::calc_eta(float dif, float bytes, float m_csize, float m_tsize) {
	if (m_csize == 0 or dif < 0.001) { return "--:--"; }
	float rate = (m_csize / dif);
	int eta = ((m_tsize - m_csize) / rate);

return format_duration(eta);
}

