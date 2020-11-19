#include "PI_Tools.hpp"

namespace PI_Tools
{
	void toClipboard(const std::string& s)
	{
		// ATTENTION: THIS FUNCTION MAY NOT WORK AS EXPECTED!!!
		HWND hwnd = GetDesktopWindow();
		OpenClipboard(hwnd);
		EmptyClipboard();
		HGLOBAL hg = GlobalAlloc(GMEM_MOVEABLE, s.size() + 1);
		if (!hg)
		{
			CloseClipboard();
			return;
		}
		memcpy(GlobalLock(hg), s.c_str(), s.size() + 1);
		GlobalUnlock(hg);
		SetClipboardData(CF_TEXT, hg);
		CloseClipboard();
		GlobalFree(hg);
		return;
	}

	void UTF8Input(std::string& s)
	{
		wchar_t wstr[255];
		char mb_str[255 * 3 + 1];
		unsigned long read;
		void* con = GetStdHandle(STD_INPUT_HANDLE);
		ReadConsole(con, wstr, 255, &read, NULL);
		int size = WideCharToMultiByte(CP_UTF8, 0, wstr, read, mb_str, sizeof(mb_str), NULL, NULL);
		mb_str[size] = 0;
		s = mb_str;
		return;
	}

	void curl::curl_send(std::string URL, std::string* preHeaders, short int preHeadersNum, std::string& retVar, std::string customReq, bool header, std::string data, std::string cookie, std::string referer, std::string userAgent)
	{
		struct curl_slist* headers = NULL;
		headers = curl_slist_append(headers, "charset: utf-8");
		for (int i = 0; i < preHeadersNum; ++i)
		{
			headers = curl_slist_append(headers, preHeaders[i].c_str());
		}
		CURL* curl = curl_easy_init();
		CURLcode res;
		if (curl)
		{
			curl_easy_setopt(curl, CURLOPT_URL, URL.c_str());
			curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
			if (customReq == "POST")
			{
				curl_easy_setopt(curl, CURLOPT_POST, 1);
			}
			else if (customReq != "GET")
			{
				curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, customReq.c_str());
			}
			if (data != "")
			{
				curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
			}
			if (header != false)
			{
				curl_easy_setopt(curl, CURLOPT_HEADER, 1);
				curl_easy_setopt(curl, CURLOPT_NOBODY, 1);
			}
			if (referer != "")
			{
				curl_easy_setopt(curl, CURLOPT_REFERER, referer.c_str());
			}
			if (cookie != "")
			{
				curl_easy_setopt(curl, CURLOPT_COOKIE, cookie.c_str());
			}
			curl_easy_setopt(curl, CURLOPT_USERAGENT, userAgent.c_str());
			curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curl::write_callback);
			curl_easy_setopt(curl, CURLOPT_WRITEDATA, &retVar);
			res = curl_easy_perform(curl);
			curl_easy_cleanup(curl);
		}
		return;
	}
}
