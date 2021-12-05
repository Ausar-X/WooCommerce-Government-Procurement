#!/usr/bin/env python3
# -*- coding: utf-8 -*

# Version: 1.0

# Prerequisites:
#apt install python3-zeep python3-pymysql -y
#
#CREATE TABLE pp (ppbh CHAR(32) NOT NULL, ppmc VARCHAR(640) NOT NULL, ID MEDIUMINT(2) UNSIGNED NOT NULL);
#CREATE TABLE pm (pmbh CHAR(24) NOT NULL, pmmc VARCHAR(640) NOT NULL, ID MEDIUMINT(2) UNSIGNED NOT NULL);
#CREATE TABLE lb (lbbh CHAR(20) NOT NULL, lbmc VARCHAR(640) NOT NULL, ID MEDIUMINT(2) UNSIGNED NOT NULL);
#CREATE TABLE categories (lbbh CHAR(16) NOT NULL, lbmc VARCHAR(320) NOT NULL, ID MEDIUMINT(2) UNSIGNED NOT NULL);
# ATTENTION: IN SOME CASES: CREATE TABLE lb (lbbh VARCHAR(32) NOT NULL, lbmc VARCHAR(640) NOT NULL, ID MEDIUMINT(2) UNSIGNED NOT NULL);

from zeep import Client
from zeep.transports import Transport
import argparse, base64, json, pymysql.cursors, requests, sys

parser = argparse.ArgumentParser(description="Henan Raytonne Trading Company Product Management API")
parser.add_argument("-O", "--Operation", help="basic operations", required=True)
parser.add_argument("-I", "--ID", help="product ID (a.k.a xhbh)", required=False)
parser.add_argument("-i", "--id", help="WooCommerce product id", required=False)
parser.add_argument("-p", "--price", help="product pricing", required=False)
parser.add_argument("-d", "--description", help="product descriptions", required=False)
args = vars(parser.parse_args())

REST_USR = "WooCommerce_REST_API_User"
REST_PWD = "WooCommerce_REST_API_Password"
REST_HST = "https://raytonne.com"

DB_USR = "Database_User"
DB_PWD = "Database_Password"
DB_NME = "Database_Name"
DB_HST = "Database_Hostname"
mysqlConn = pymysql.connect(host=DB_HST, user=DB_USR, password=DB_PWD, db=DB_NME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

def error_exit(retVal = "ERR"):
	mysqlConn.close()
	sys.exit(retVal)

def _base64(ogStr, encode = False):
	if encode == True:
		return base64.b64encode(ogStr.encode("utf-8")).decode("ascii")
	else:
		ogStr += "=" * ((4 - len(ogStr) % 4) % 4)
		return base64.b64decode(ogStr.encode("ascii")).decode("utf-8")

'''
def category_name(pmbh):
	try:
		URLSource = requests.get("http://222.143.21.205:8081/", timeout=10).text.split("<dt class=\"cat-name\"> <a href='JavaScript:void(0);' title='")
		URLSource.pop(0)
	except:
		error_exit()
	retVal = ""
	for URLsource in URLSource:
		if _base64(pmbh, True) in URLsource:
			retVal = URLsource.split("'")[0]
			break;
	if retVal != "":
		return retVal
	else:
		error_exit()
'''

def core_component(jData, action):
	if type(jData) is str:
		with open(jData, encoding="utf-8") as json_data_temp:
			queryData = str(json.load(json_data_temp))
	else:
		queryData = json.dumps(jData, ensure_ascii = False)
	wsdl_url = "http://222.143.21.205:8099/wsscservices/services/wsscWebService?wsdl"
	soap_client = Client(wsdl_url, transport = Transport(timeout=10))
	queryFunction = "soap_client.service." + action + "(queryData)"
	queryData = eval(queryFunction)
	queryData = json.loads(queryData)
	return queryData

if args["Operation"] == "new":
	json_data = {}
	json_data["username"] = "YOUR_ASSIGNED_GP_USERNAME"
	json_data["pwd"] = "YOUR_ASSIGNED_GP_USERNAME"
	json_data["xhbh"] = args["ID"]
	try:
		Data = core_component(json_data, "findSpByXhbh")
	except:
		error_exit()
	if Data["resultFlag"] == "Y":
		try:
			with mysqlConn.cursor() as cursor:
				sql = "SELECT `ppmc`, `ID` FROM `pp` WHERE `ppbh`=%s"
				cursor.execute(sql, (Data["ppbh"],))
				result = cursor.fetchone()
				if result == None:
					RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/tags", json={"name": Data["ppmc"], "slug": Data["ppbh"]}, auth=(REST_USR, REST_PWD), timeout=3).json()
					if RESTRet and 'id' in RESTRet:
						sql = "INSERT INTO `pp` (`ppbh`, `ppmc`, `ID`) VALUES (%s, %s, %s)"
						cursor.execute(sql, (Data["ppbh"], Data["ppmc"], RESTRet['id']))
						mysqlConn.commit()
						tagID = int(RESTRet['id'])
					else:
						error_exit()
				elif result['ppmc'] != Data["ppmc"]:
					RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/tags/" + str(result['ID']), json={"name": Data["ppmc"]}, auth=(REST_USR, REST_PWD), timeout=3).json()
					if RESTRet and 'id' in RESTRet:
						sql = "UPDATE `pp` set `ppmc` = %s WHERE `ppbh` = %s"
						cursor.execute(sql, (Data["ppmc"], Data["ppbh"]))
						mysqlConn.commit()
						tagID = int(RESTRet['id'])
					else:
						error_exit()
				else:
					tagID = int(result["ID"])

				sql = "SELECT `pmmc`, `ID` FROM `pm` WHERE `pmbh`=%s"
				cursor.execute(sql, (Data["pmbh"],))
				result = cursor.fetchone()
				if result == None:
					error_exit()
					'''
					sql = "SELECT `lbmc`, `ID` FROM `lb` WHERE `lbbh`=%s"
					cursor.execute(sql, (Data["lbbh"],))
					result = cursor.fetchone()
					if result == None:
						sql = "SELECT `lbmc`, `ID` FROM `categories` WHERE `lbbh`=%s"
						cursor.execute(sql, (Data["pmbh"][:16],))
						result = cursor.fetchone()
						categoryName = category_name(Data["pmbh"])
						if result == None:
							RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": categoryName, "slug": Data["pmbh"][:16]}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "INSERT INTO `categories` (`lbbh`, `lbmc`, `ID`) VALUES (%s, %s, %s)"
								cursor.execute(sql, (Data["pmbh"][:16], categoryName, RESTRet['id']))
								mysqlConn.commit()
								catID = int(RESTRet['id'])
							else:
								error_exit()
						elif result['lbmc'] != categoryName:
							RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": categoryName}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "UPDATE `categories` set `lbmc` = %s WHERE `lbbh` = %s"
								cursor.execute(sql, (categoryName, Data["pmbh"][:16]))
								mysqlConn.commit()
								catID = int(RESTRet['id'])
							else:
								error_exit()
						else:
							catID = int(result["ID"])
						RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": Data["lbmc"], "slug": Data["lbbh"], "parent": catID}, auth=(REST_USR, REST_PWD), timeout=3).json()
						if RESTRet and 'id' in RESTRet:
							sql = "INSERT INTO `lb` (`lbbh`, `lbmc`, `ID`) VALUES (%s, %s, %s)"
							cursor.execute(sql, (Data["lbbh"], Data["lbmc"], RESTRet['id']))
							mysqlConn.commit()
							catID = int(RESTRet['id'])
						else:
							error_exit()
					elif result['lbmc'] != Data["lbmc"]:
						RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": Data["lbmc"]}, auth=(REST_USR, REST_PWD), timeout=3).json()
						if RESTRet and 'id' in RESTRet:
							sql = "UPDATE `lb` set `lbmc` = %s WHERE `lbbh` = %s"
							cursor.execute(sql, (Data["lbmc"], Data["lbbh"]))
							mysqlConn.commit()
							catID = int(RESTRet['id'])
						else:
							error_exit()
					else:
						catID = int(result["ID"])
					RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": Data["pmmc"], "slug": Data["pmbh"], "parent": catID}, auth=(REST_USR, REST_PWD), timeout=3).json()
					if RESTRet and 'id' in RESTRet:
						sql = "INSERT INTO `pm` (`pmbh`, `pmmc`, `ID`) VALUES (%s, %s, %s)"
						cursor.execute(sql, (Data["pmbh"], Data["pmmc"], RESTRet['id']))
						mysqlConn.commit()
						catID = int(RESTRet['id'])
					else:
						error_exit()
				elif result['pmmc'] != Data["pmmc"]:
					RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": Data["pmmc"]}, auth=(REST_USR, REST_PWD), timeout=3).json()
					if RESTRet and 'id' in RESTRet:
						sql = "UPDATE `pm` set `pmmc` = %s WHERE `pmbh` = %s"
						cursor.execute(sql, (Data["pmmc"], Data["pmbh"]))
						mysqlConn.commit()
						catID = int(RESTRet['id'])
					else:
						error_exit()
					'''
				else:
					catID = int(result["ID"])

			if (args["description"] == None) or (args["description"] == ""):
				RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products", json={"name": Data["xhmc"], "type": "simple", "regular_price": str(args["price"]), "categories": [{"id": catID}], "tags": [{"id": tagID}], "slug": args["ID"], "sku": "G" + args["ID"]}, auth=(REST_USR, REST_PWD), timeout=3).json()
			else:
				RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products", json={"name": Data["xhmc"], "type": "simple", "regular_price": str(args["price"]), "categories": [{"id": catID}], "tags": [{"id": tagID}], "slug": args["ID"], "sku": "G" + args["ID"], "description": _base64(args["description"])}, auth=(REST_USR, REST_PWD), timeout=3).json()
			if RESTRet and 'id' in RESTRet:
				mysqlConn.close()
				print("OK")
			else:
				error_exit()
		except:
			error_exit()
	else:
		error_exit()

elif args["Operation"] == "delete":
	try:
		RESTRet = requests.delete(REST_HST + "/wp-json/wc/v3/products/" + str(args["id"]) + "?force=true", auth=(REST_USR, REST_PWD), timeout=3).json()
		if RESTRet and 'id' in RESTRet:
			mysqlConn.close()
			print("OK")
		else:
			error_exit()
	except:
		error_exit()

elif args["Operation"] == "updateCat":
	try:
		URLSource = requests.get("http://222.143.21.205:8081/", timeout=10).text.split("<dt class=\"cat-name\"> <a href='JavaScript:void(0);' title='")
		URLSource.pop(0)
	except:
		error_exit()
	with mysqlConn.cursor() as cursor:
		for URLsource in URLSource:
			category = URLsource.split("'")[0]
			URLSource2 = URLsource.split('<dt> <a href="JavaScript:void(0);" title="')
			URLSource2.pop(0)
			A = 0
			for URLsource2 in URLSource2:
				categoryLB = URLsource2.split('"')[0]
				URLSource3 = URLsource2.split("/category/products?pmbh=")
				URLSource3.pop(0)
				a = 0
				for URLsource3 in URLSource3:
					categorypm = _base64(URLsource3.split('"')[0])[:24]
					categoryPM = URLsource3.split('target="_self" title="')[1].split('"')[0]
					if A == 0:
						sql = "SELECT `lbmc`, `ID` FROM `categories` WHERE `lbbh`=%s"
						cursor.execute(sql, (categorypm[:16],))
						result = cursor.fetchone()
						if result == None:
							RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": category, "slug": categorypm[:16]}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "INSERT INTO `categories` (`lbbh`, `lbmc`, `ID`) VALUES (%s, %s, %s)"
								cursor.execute(sql, (categorypm[:16], category, RESTRet['id']))
								mysqlConn.commit()
								AID = int(RESTRet['id'])
							else:
								error_exit()
						elif result['lbmc'] != category:
							RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": category}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "UPDATE `categories` set `lbmc` = %s WHERE `lbbh` = %s"
								cursor.execute(sql, (category, categorypm[:16]))
								mysqlConn.commit()
								AID = int(RESTRet['id'])
							else:
								error_exit()
						else:
							AID = int(result["ID"])
						A = 1
					if a == 0:
						sql = "SELECT `lbmc`, `ID` FROM `lb` WHERE `lbbh`=%s"
						cursor.execute(sql, (categorypm[:20],))
						result = cursor.fetchone()
						if result == None:
							RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": categoryLB, "slug": categorypm[:20], "parent": AID}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "INSERT INTO `lb` (`lbbh`, `lbmc`, `ID`) VALUES (%s, %s, %s)"
								cursor.execute(sql, (categorypm[:20], categoryLB, RESTRet['id']))
								mysqlConn.commit()
								aID = int(RESTRet['id'])
							else:
								error_exit()
						elif result['lbmc'] != categoryLB:
							RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": categoryLB}, auth=(REST_USR, REST_PWD), timeout=3).json()
							if RESTRet and 'id' in RESTRet:
								sql = "UPDATE `lb` set `lbmc` = %s WHERE `lbbh` = %s"
								cursor.execute(sql, (categoryLB, categorypm[:20]))
								mysqlConn.commit()
								aID = int(RESTRet['id'])
							else:
								error_exit()
						else:
							aID = int(result["ID"])
						a = 1
					sql = "SELECT `pmmc`, `ID` FROM `pm` WHERE `pmbh`=%s"
					cursor.execute(sql, (categorypm,))
					result = cursor.fetchone()
					if result == None:
						RESTRet = requests.post(REST_HST + "/wp-json/wc/v3/products/categories", json={"name": categoryPM, "slug": categorypm, "parent": aID}, auth=(REST_USR, REST_PWD), timeout=3).json()
						if RESTRet and 'id' in RESTRet:
							sql = "INSERT INTO `pm` (`pmbh`, `pmmc`, `ID`) VALUES (%s, %s, %s)"
							cursor.execute(sql, (categorypm, categoryPM, RESTRet['id']))
							mysqlConn.commit()
						else:
							error_exit()
					elif result['pmmc'] != categoryPM:
						RESTRet = requests.put(REST_HST + "/wp-json/wc/v3/products/categories/" + str(result['ID']), json={"name": categoryPM}, auth=(REST_USR, REST_PWD), timeout=3).json()
						if RESTRet and 'id' in RESTRet:
							sql = "UPDATE `pm` set `pmmc` = %s WHERE `pmbh` = %s"
							cursor.execute(sql, (categoryPM, categorypm))
							mysqlConn.commit()
						else:
							error_exit()
