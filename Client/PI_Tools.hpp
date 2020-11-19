#ifndef PI_TOOLS_H_
#define PI_TOOLS_H_

#include <string>
#include <Windows.h>
#include <curl/curl.h>

namespace PI_Tools
{
	void toClipboard(const std::string& s);

	void UTF8Input(std::string & s);

	class curl
	{
	public:
		static size_t write_callback(void* contents, size_t size, size_t nmemb, void* userp)
		{
			((std::string*)userp)->append((char*)contents, size * nmemb);
			return size * nmemb;
		}
		void curl_send(std::string URL, std::string* preHeaders, short int preHeadersNum, std::string& retVar, std::string customReq = "GET", bool header = false, std::string data = "", std::string cookie = "", std::string referer = "", std::string userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36");
	};
}

#endif
