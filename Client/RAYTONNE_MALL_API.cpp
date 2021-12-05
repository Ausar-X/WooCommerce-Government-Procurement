#include <iostream>
#include <regex>
#define NOMINMAX
#include "PI_Tools.hpp"
#include <wininet.h>
#pragma comment(lib,"Wininet.lib")

// Version: 1.0

using namespace std;

int main()
{
	SetConsoleOutputCP(CP_UTF8);
	SetConsoleCP(CP_UTF8);

	PI_Tools::curl easy_curl;
	char* c_or_d = (char*)malloc(2);
	const char* CD = "CDQ";

	double price = 0;
	string preHeaders[1] = { "" };
	string WooCommerceRet = "", errMsg = "", imgURL = "", enxiProductID = "", productPrice = "", productDesc = "", productURL = "", postData = "";
	size_t subStrStart, subStrEnd;
	regex regexMatchImgURL("(jqimg=\")(http.*g)(\" src)");
	smatch regexMatchImgURLRes;

	cout << "Government Procurement & WooCommerce API" << endl;
	cout << "Copyright 2021 Henan Raytonne Trading Company. All rights reserved." << endl;
	cout << "\nOfficial Website: https://raytonne.com/" << endl;
	cout << "License: GNU GPLv3" << endl;
	cout << "GitHub Repo: https://github.com/ausar-x/WooCommerce-Government-Procurement" << endl;
	cout << "Should you need any further information, please do not hesitate to contact us.\n" << endl;

	cout << "Do you want to create or delete a product (type q for quit)? [c/d/q] ";
	while ((!(cin >> c_or_d)) || ((toupper(c_or_d[0]) != CD[0]) && (toupper(c_or_d[0]) != CD[1]) && (toupper(c_or_d[0]) != CD[2])))
	{
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cout << "Do you want to create or delete a product (type q for quit)? [c/d/q] ";
	}
	cin.clear();
	cin.ignore(numeric_limits<streamsize>::max(), '\n');

	while (toupper(c_or_d[0]) != CD[2])
	{
		cout << "Please enter the URL: ";
		getline(cin, productURL);
		while (productURL.empty())
		{
			cout << "Please enter the URL: ";
			getline(cin, productURL);
		}
		bool testConn1 = InternetCheckConnection(L"http://222.143.21.205:8081/", FLAG_ICC_FORCE_CONNECTION, 0);
		bool testConn2 = InternetCheckConnection(L"https://api.example.com/", FLAG_ICC_FORCE_CONNECTION, 0);
		if (!testConn1 || !testConn2)
		{
			cout << "\n\nError:\nCould not establish connection to server." << endl;
		}
		if (toupper(c_or_d[0]) == CD[0])
		{
			easy_curl.curl_send("http://222.143.21.205:8081/", preHeaders, 0, WooCommerceRet, "GET", true);
			subStrStart = WooCommerceRet.find("SESSION=");
			subStrEnd = WooCommerceRet.find(";", subStrStart);
			if (subStrStart != string::npos && subStrEnd != string::npos)
			{
				WooCommerceRet = WooCommerceRet.substr(subStrStart, subStrEnd - subStrStart);
			}
			else
			{
				errMsg = "Could not retrieve cookie values.";
				goto ERRLABEL;
			}
			easy_curl.curl_send(productURL, preHeaders, 0, WooCommerceRet, "GET", false, "", WooCommerceRet, "http://222.143.21.205:8081/");
			if (regex_search(WooCommerceRet, regexMatchImgURLRes, regexMatchImgURL)) {
				imgURL = regexMatchImgURLRes[2];
			}
			subStrStart = WooCommerceRet.find("data[\"xhbh\"] = \"");
			subStrStart = WooCommerceRet.find("data[\"xhbh\"] = \"", subStrStart + 1);
			subStrEnd = WooCommerceRet.find("\";", subStrStart);
			if (subStrStart != string::npos && subStrEnd != string::npos)
			{
				enxiProductID = WooCommerceRet.substr(subStrStart, subStrEnd - subStrStart);
				enxiProductID.erase(0, 16);
			}
			cout << "Do you want to set a different price? Please leave it blank to skip; otherwise, please enter it here: ";
			getline(cin, productPrice);
			if (productPrice.empty()) {
				subStrStart = WooCommerceRet.find(" index_num = ''+");
				subStrEnd = WooCommerceRet.find(";", subStrStart);
				if (subStrStart != string::npos && subStrEnd != string::npos)
				{
					productPrice = WooCommerceRet.substr(subStrStart, subStrEnd - subStrStart);
					productPrice.erase(0, 16);
				}
			}
			else
			{
				try {
					price = ceil(stod(productPrice) * 100.0) / 100.0;
					productPrice = to_string(price);
					productPrice.erase(productPrice.find_last_not_of('0') + 1, string::npos);
				}
				catch (...)
				{
					productPrice = "";
				}
			}
			subStrStart = WooCommerceRet.find("f second-color\">");
			subStrEnd = WooCommerceRet.find("</p>", subStrStart);
			if (subStrStart != string::npos && subStrEnd != string::npos)
			{
				productDesc = WooCommerceRet.substr(subStrStart, subStrEnd - subStrStart);
				productDesc.erase(0, 16);
			}
			WooCommerceRet = "";
			if (imgURL == "" || enxiProductID == "" || productPrice == "")
			{
				errMsg = "Could not retrieve product information.";
				imgURL = enxiProductID = productPrice = "";
				goto ERRLABEL;
			}
			else
			{
				postData = "pwd=YOUR_PASSWORD_HERE&productID=" + enxiProductID + "&productImg=" + imgURL + "&productPrice=" + productPrice;
			}
			if (productDesc != "")
			{
				postData += "&productDesc=" + regex_replace(productDesc, regex("\\r\\n|\\n"), string("<br>"));
			}
			easy_curl.curl_send("https://api.example.com/", preHeaders, 0, WooCommerceRet, "POST", false, postData);
			if (WooCommerceRet == "OK")
			{
				PI_Tools::toClipboard("http://raytonne.com/shop/" + enxiProductID + "/");
				cout << "\nSuccess: the URL has been copied to the clipboard.\n" << endl;
			}
			else
			{
				cout << "\nFailed to create the new product, please try again later.\n" << endl;
			}
		ERRLABEL:
			if (errMsg != "")
			{
				cout << "\n\nError:\n" << errMsg << "\n\n";
				errMsg = "";
			}
		}
		else
		{
			postData = "delete=yes&pwd=YOUR_PASSWORD_HERE&productURL=" + productURL;
			easy_curl.curl_send("https://api.example.com/", preHeaders, 0, WooCommerceRet, "POST", false, postData);
			if (WooCommerceRet == "OK")
			{
				cout << "\nSuccess: the product has been deleted.\n" << endl;
			}
			else
			{
				cout << "\nFailed to delete the product, please try again later.\n" << endl;
			}
		}
		WooCommerceRet = imgURL = enxiProductID = productPrice = productDesc = productURL = "";
		price = 0;
		cout << "Do you want to create or delete a product (type q for quit)? [c/d/q] ";
		while ((!(cin >> c_or_d)) || ((toupper(c_or_d[0]) != CD[0]) && (toupper(c_or_d[0]) != CD[1]) && (toupper(c_or_d[0]) != CD[2])))
		{
			cin.clear();
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			cout << "Do you want to create or delete a product (type q for quit)? [c/d/q] ";
		}
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
	}
	return 0;
}
