import requests
from bs4 import BeautifulSoup
import urllib
from sites.mouser import Mouser
import re


class Scrapper(Mouser):

    def scrap_onsemi(self, partnumber):
        try:
            response = requests.get(
                "https://www.onsemi.com/PowerSolutions/MaterialComposition.do?searchParts=" + urllib.parse.quote(str(partnumber), safe=''))
            data = BeautifulSoup(response.text, 'lxml')
            table = data.find(id="MaterialCompositionTable")
            pn = table.tbody.tr.td.find_next('td').text
            status = table.tbody.tr.td.find_next('td').find_next('td').text
            hf = table.tbody.tr.td.find_next(
                'td').find_next('td').find_next('td').text
            excempt = table.tbody.tr.td.find_next('td').find_next(
                'td').find_next('td').find_next('td').text
            links = table.find_all('a', href=True)
            declaration = "https://www.onsemi.com" + links[5]['href']
            lead = "not found"
            if len(excempt) > 1:
                lead = table.tbody.tr.td.find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                    'td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').text

            return {"Results": "Found", "SPN_grabbed": pn, "Status": status, "HF": hf, "Excemption": excempt, "Declaration": declaration, "Lead(Cas No:7439-92-1)": lead}

        except Exception as e:
            return {"status": 404}

    def scrap_Maxim(self, partnumber):
        part = re.sub.replace(":", "/", partnumber)
        print(part)
        url = requests.get(
            "https://www.maximintegrated.com/en/qa-reliability/emmi/content-lookup/product-content-info.html?partNumber=" + urllib.parse.quote(str(part)))
        soup = BeautifulSoup(url.text, 'lxml')
        try:
            table = soup.find(id="productcontentinfo")
            Rohs_Compliance = table.tbody.tr.td.find_next('td').text
            Rohs2_compliance = table.tbody.tr.td.find_next(
                'tr').td.find_next('td').text
            Halogen_compliance = table.tbody.tr.find_next(
                'tr').find_next('tr').td.find_next('td').text
            Reach_Compliance = table.tbody.tr.find_next('tr').find_next(
                'tr').find_next('tr').td.find_next('td').text
            print(Rohs_Compliance, Rohs2_compliance,
                  Halogen_compliance, Reach_Compliance)
            return {"Results": "Found", "Partnumber": part, "Rohs_Compliance": Rohs_Compliance, "Rohs2_compliance": Rohs2_compliance, "Halogen_compliance": Halogen_compliance, "Reach_Compliance": Reach_Compliance}
        except Exception as e:
            print(e)
            return {"status": 404}

    def scrap_Molex(self, partnumber):
        url = "https://www.molex.com/molex/search/partSearch?query=" + \
            urllib.parse.quote(str(partnumber), safe="") + "&pQuery="
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        try:
            mpn = soup.find("div", class_="col-md-10").find("h1").text
            partname = soup.find(
                "div", class_="col-md-10").find("p", class_="subtitle").text
            status = soup.find("p", class_="info").text
            series = soup.find("a", class_='text-link').text
            rohs = soup.find(
                "div", id="tab-environmental").find_all("p")[1].text
            reach = soup.find(
                "div", id="tab-environmental").find_all("p")[3].text
            halogen = soup.find(
                "div", id="tab-environmental").find_all("p")[4].text
            link = soup.find(
                "div", id="tab-environmental").find_all("p")[8].find("a", href=True)
            declaration = link['href']
            return {"Results": "Found", "MPN": mpn, "PArtname": partname, "Status": status, "Series": series, "ROHS": rohs, "REACH": reach, "HALOGEN": halogen, "Declaration": declaration}
        except Exception as e:

            return {"status": 404}

    def scrap_Phoenix(self, partnumber):
        try:
            url = "https://www.phoenixcontact.com/customer/api/v1/product-compliance/products?_locale=en-CA&_realm=ca&offset=0&requestedSize=11"
            reporturl = "https://www.phoenixcontact.com/customer/api/v1/product-compliance/report/guid?_locale=en-CA&_realm=ca"

            #payload = "{\"searchItems\":[\"1084745\"]}"
            payload = '{\"searchItems\":[\"' + \
                urllib.parse.quote(str(partnumber)) + '\"]}'
            headers = {
                'authority': 'www.phoenixcontact.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en;q=0.9,de;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://www.phoenixcontact.com',
                'pragma': 'no-cache',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', }
            response = requests.request(
                "POST", url, headers=headers, data=payload)
            report_response = requests.request(
                "POST", reporturl, headers=headers, data=payload)
            link = "https://www.phoenixcontact.com/customer/api/v1/product-compliance/report/guid/" + \
                report_response.text + "?_locale=en-US&_realm=us"

            res = response.json()

            for results in res['items'].values():

                if results["validItem"] == False:
                    return {"status": 404}
                else:
                    return results
        except Exception as e:
            print(e)
            return {status: 404}

    def scrap_Rscomponents(self, partnumber):
        try:
            url = "https://export.rsdelivers.com/productlist/search?query=" + \
                urllib.parse.quote(str(partnumber))

            r = requests.get(url)
            data = BeautifulSoup(r.text, 'lxml')
            partName = data.find(
                "h1", class_='product-detail-page-component_title__HAXxV').text

            manufacturerName = data.find("div", class_='pill-component-module_grey__38ctb').find_next(
                "div", class_='pill-component-module_grey__38ctb').text

            mpn = data.find("div", class_='pill-component-module_grey__38ctb').find_next(
                "div", class_='pill-component-module_grey__38ctb').find_next("div", class_='pill-component-module_grey__38ctb').text

            return {"Results": "Found", "Partnumber": partnumber, "mpn": mpn, "partName": partName, "manufacturerName": manufacturerName}
        except Exception as e:
            print(e)
            return {"status": 404}

    def scrap_Te(self, partnumber):
        try:
            url = "https://www.te.com/commerce/alt/ValidateParts.do"

            payload = 'partNumber=' + partnumber
            headers = {
                'authority': 'www.te.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'en-US,en;q=0.9',
                'cache-control': 'max-age=0',
                'content-type': 'application/x-www-form-urlencoded',
                'referer': 'https://www.te.com/commerce/alt/product-compliance.do',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
                'Access-Control-Request-Method': '*',
                'x-requested-with': 'XMLHttpRequest'

            }

            response = requests.request(
                "POST", url, headers=headers, data=payload)
            soup = BeautifulSoup(response.text, 'lxml')
            tePartNum = soup.find('div', class_='product_description').text
            status = soup.find('table').find('tbody').find('tr').find(
                'td').find('a').find_next('a').find_next('a').text
            rohsInfo = soup.find('table').find('tbody').find('tr').find(
                'td').find_next('td').find('div', class_='compliance').find('a').text
            # try:
            rohsExcemption = soup.find('table').find('tbody').find('tr').find(
                'td').find_next('td').find('div', class_='compliance').find('div', style='margin-top:8px;').text

            # except Exception:
            # pass
            current_reach_candidate = soup.find('table').find('tbody').find('tr').find('td').find_next('td').find('div', class_='compliance').find_next(
                'div', class_='compliance').find_next('div', class_='compliance').find_next('div', class_='compliance').find('span').text
            current_reach_declaration = soup.find('table').find('tbody').find('tr').find('td').find_next('td').find('div', class_='compliance').find_next(
                'div', class_='compliance').find_next('div', class_='compliance').find_next('div', class_='compliance').find('span').find_next('span').text
            svhc = soup.find('table').find('tbody').find('tr').find('td').find_next('td').find('div', class_='compliance').find_next(
                'div', class_='compliance').find_next('div', class_='compliance').find_next('div', class_='compliance').find('span').find_next('span').find_next('span').text
            return {"Results": "Found", "Status": status, "TE-PartNum": tePartNum, "rohsInfo": rohsInfo,
                    "rohs-excemption": rohsExcemption, "reach-candidate": current_reach_candidate, "rewach-declaration": current_reach_declaration, "svhc": svhc, "declaration-link": 'https://www.te.com/commerce/alt/SinglePartSearch.do?PN='+tePartNum+'&dest=stmt'}
        except Exception as e:
            print(e)
            return {"status": 404}

    def scrap_Wago(self, partnumber):
        url = requests.get("https://smartdata.wago.com/articledata/svhc?articleNr=" +
                           urllib.parse.quote(str(partnumber), safe="") + "&country=Germany")
        soup = BeautifulSoup(url.text, 'lxml')
        try:

            table = soup.find(id="articleList")

            spn_grabbed = table.tbody.tr.td.text
            description = table.tbody.tr.td.find_next('td').text
            reach_substance = table.tbody.tr.td.find_next(
                'td').find_next('td').text
            scip = table.tbody.tr.td.find_next(
                'td').find_next('td').find_next('td').text
            cas_no = table.tbody.tr.td.find_next('td').find_next(
                'td').find_next('td').find_next('td').text
            rohs_status = table.tbody.tr.td.find_next('td').find_next(
                'td').find_next('td').find_next('td').find_next('td').text
            rohs_exception = table.tbody.tr.td.find_next('td').find_next('td').find_next(
                'td').find_next('td').find_next('td').find_next('td').text

            return {"Results": "Found", "Partnumber": partnumber, "PartName": description, "SPN_grabbed": spn_grabbed, "Reach": reach_substance, "Scip": scip, "Cas_no": cas_no, "ROHS_Exception": rohs_exception, "ROHS_Status": rohs_status, "Declaration": "https://smartdata.wago.com/articledata/svhc/download?articleNr=" + spn_grabbed + "&country=Austria"}

        except Exception as e:
            print(e)
            return {"status": 404}

    def scrap_omron(self, partnumber):
        try:
            url = "https://industrial.omron.eu/en/api/rohs_reach/search.json?q=" + \
                str(partnumber) + "&page=1"
            payload = {}
            headers = {
                'authority': 'industrial.omron.eu',
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'en-US,en;q=0.9',
                # 'cookie': 'OMR_USER_LANG=EU-en; _gcl_au=1.1.1823097155.1661233578; _ga=GA1.3.1108793817.1661233578; _gid=GA1.3.1802832004.1661233578; nQ_cookieId=6a1bd137-c19e-3e85-c194-42f967dcb5dc; nQ_userVisitId=516dbf5b-534c-5333-a722-578b538d38a0; AMCVS_7FCC6D075DDD2B730A495C72%40AdobeOrg=1; AMCV_7FCC6D075DDD2B730A495C72%40AdobeOrg=-432600572%7CMCIDTS%7C19228%7CMCMID%7C51015238740838683563499486990667075736%7CMCAAMLH-1661838380%7C6%7CMCAAMB-1661838380%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1661240780s%7CNONE%7CvVersion%7C4.5.2; tracking_enabled=true; updated_bar=true; s_cc=true; ELOQUA=GUID=6255A7F231D5496BB717432E9D0FC266; _navigation=60ba1233651a71dfcde6938d71ca7b99db31fc7c; stat_track_u_id=uid%3D915270800%26f%3D5373%253A1022%26st%3D1%26sy%3D%26ls%3D1661244382%26off%3D%26noacts%3D%26dg%3D%26hs%3D1; _stat_track_s_id=_si%3D1661233584%26_sid%3D1661244382%26_inew%3D1%26_ls%3D1661244382%26_lurl%3D1785484693%26_lrfr%3D1785484693%26_la%3D1661244760%26_so%3D%26_pp%3D%26_bh%3D382%26_ane%3D%26_te%3D%26_nay%3D%26_nae%3D%26_nac%3D; s_ips=1077; s_sq=%5B%5BB%5D%5D; _session=4Mc37rGQbTiSFsNImDbzzfBBcl7%2FHA%2Bykdok08VY0UZaAJ8skC95teMB6tLb0sI0bVCgHTDiBnAZX9Jor%2BC2Xnho%2BDZbmCw%2FljXDYjr6HgTVl%2FJdvaxQT%2Fxd8nO5X5JCxq78INmknLPReBPmBA8RpxYx8X3xY3XLJnl3qStDxFO%2BDEN8I9EsmBrFbP4kA4u0j7bS%2BaI0FXnzwEVGJaTvd6dNbcR8gNwwidTmgVZCwanIt9XH6zX8ouKcwGzuVBPiSZmjiu3y5t7HHTozmFnwQtE8s2hbhoeUs0ZZoco4FK3AKNUL0sstxxZ9PXKelr6VSZjSWuir9yjknLDrstu1RD2i95ok4w2i%2Bb%2FsfDbWlmWprJlpW3IYLRl3380cupSkoyPbeRKHFL6ipi1Mwh%2BvfFJ8t77g9hFkuFcFKcrZw3qk0y2TstGcghfNYB5rKhj2vL9cA%2BKS0DkKbfyTSlqqq7cG7xlYoysXR19V7TlivLiqK%2Fyc3cXvoo7xMJVC4xKhP6qZtK5z9XuWArE8b8VGksKg6efm46Lh2SC8Bi8MsIb%2FGA9TgpItsQw%2BzZFRIeYNMh13OmuaHdNWfHzaO845hw%2B0ozKxa7VS8qY%2Fm4dTv0qKV%2BJL2SJFM2uRTpEVqKae6gMq5TL%2FGt1He9%2BnCgAOyuR8NTVTDISjrvMQM1TY5%2BfSsmRZB%2F807Ac1Cvf5%2FjOFwhEGgIznaX3onDA3h0WZc7UZDafiGRfGIEvBy1m8t%2BZbqt8dc9uTE68w3hlBQB8%2BW1iC7KmhQwb7ouRdXFIZSqMMeX5QxLrNY4JsfoQ5TpQfu%2Bup0YhI4ZZFm%2Fc0xhS76POOhiTq4NvwlhAJ%2BriJwbWWTXEp9lSbKfGiuEXksHG9w3rW%2Fc4lXA02kxBAbGFlKPGWPLr%2B1CEw8Xd4sGketj1p2lS%2F5lb9uMopYTMa5CreQwoqcM3s%2FgS757fcVb3HPBRbYHlhhc6vpVOSqEeP1uP1oPweP6FWa06nBKM8ONCbrbADxptRnOP6FYwDtLXYLrrU9cqWZCfGi8f6%2BC5vkWot--58sY8NsqHgQGAEqy--%2Bw6DkPGXRivhoeQC4nY%2FvA%3D%3D; s_tp=1814; s_ppv=industrialeu%253Aen%253Aservices-support%253Asupport%253Aenvironmental-product-information%2C59%2C59%2C1077%2C1%2C3; OMR_USER_LANG=EU-en; _session=00ggeX7geMnlgzhSKJVrc6vSmgZ%2FABN7AjFjMWql%2Bij2ceMyV2twQDMNEv8ppUZBgPUTB4AXjnRVoapzOAMR61e1%2BY3yTamB0PWMkXOwlJi6DbrQkJpeaUTPJi40wb2cdll%2FJFrKS%2FHQJ6WGnQySdW5odvgtGqUy8tXAx4UlWymkyAM8nFlKc5xOS2RMtTBavRUXv5vzaBH3NfzjmN5u39fmq0ikB0fhCZ7sNblEPf66aWidyDTlMtgF5nLQseulUFTXhXXgwubm0HmR9Ve1uSby7AqvmGiGpjgoiiPfzTiZcbRt7H0QPHA8SDZlVSIg3oriUTsMg%2Frwybdo3oetZnedOLqxhWrciS8Nx20g7FN1zttKDuaeEQTyA%2BrW85C0GflqNlx47j%2BtvjmfsIT1janrBVNDagM4aokkZW8R34StPWAy9mobfDatKZ1nfbsp29pXL4ZjdEe6WuajCirv4VaRU2a%2BCgoGkP%2ByiQh%2BCT%2FU9Vxk29aQfVqRyFJ7iFqehnIN67S89janEs0vIxziCsW8KFVLge4tdMBBfQeL6IDi%2BQkcNO6GoMOLM5fKkm0tEW3pspRWzUwLAiYqGA3yY%2FgxsuZpqDlAw9KUlNviIsQuXDifXVb4I7%2FvOWBwR%2BkXuLJJojGh0XeZadH6oXpclq576gc%2Ffq3ZO8rxafNX8cfxAtd1tD5AAZMUBkWmw9jJzCGuyToMe%2FhFB08rAUNVpPOiKCroW8mbUJKI3n%2ByekEeyAv1EAXEzbyLYJhA6NcGukl5UQAHfx9rjn648w46n9OCk5c9wrk97nAF4SLU5AAszWSa8uCfs0TSfpRs%2FQEhi0d2zSzRHZvHqw6pRK6ZNiI9qkDujl%2FbXZFZBdwIPhZFwqabd2nrBBR9U6XCi6LsdWuagX8SJb5W8ow47o0vRyEJEPSlXUuOmHEuybjMUtWGy8LiTp9Wrje7lL8vasDB1PytQb132gLCyvv4d1C%2B55CXS%2Bh8eK0biImvxhlLP66QiC%2FUlwjRqOuPwh5HRM3%2BAXvRnSzPFTbsXiqgVQDU5MbE--2k1eRLZg0nZy9lF2--bjMe8r7ZjAp%2FsNfp%2BQzrTA%3D%3D',
                'if-none-match': 'W/"78c252489f63d35938e4b3b08d94af48"',
                'referer': 'https://industrial.omron.eu/en/services-support/support/environmental-product-information',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36',
                'x-csrf-token': 'sffvsIpH2eIPkz3qwj0Knx3QXlaKcnHsr0incPTXMqs7H0QW7RepIWyVv2qZGFz3RbCcijjDu/YKX5YeL0phFw==',
                'x-requested-with': 'XMLHttpRequest'}
            r = requests.request("GET", url, headers=headers, data=payload)
            response = r.json()
            for res in response['results']:
                if res['description'] == str(partnumber) or res['description'] == str(partnumber).replace("-", ""):
                    item_code = res['short_item_code']
                    return {"Results": "Found", "GrabbedSPN": res['description'], "RoHS 2011/65/EU": res['rohs6_compliant'], "RoHS (EU)2015/863": res['rohs10_compliant'], "SVHC contained": res['reach_substances'], "rohs-link": 'https://industrial.omron.eu/en/pdf/rohs/' + str(item_code) + '.pdf?directive=10', "reach-link": 'https://industrial.omron.eu/en/pdf/reach/' + str(item_code) + '.pdf'}
            return {"status": 404}
        except Exception as e:
            print(e)
            return {"status": 404}

    def scrap_Arrow(self, partnumber):
        url = "http://api.arrow.com/itemservice/v4/en/search/token?login=assent1&apikey=e91ee2fc20668093198daaf7252a7208e06a428b551ac2e652c83ed5671aaaee&search_token=" + \
            str(partnumber)
        payload = {}
        headers = {}
        response = requests.request(
            "GET", url, headers=headers, data=payload).json()
        results = response['itemserviceresult']['data']
        for res in results:
            try:
                for r in res['PartList']:

                    return {"Results": "Found", "MPN": r['partNum'], "Manufacturer": r['manufacturer']['mfrName']}
            except Exception as e:
                print(e)
                return {"status": 404}

    def find_Supplier(self, partnumber):

        def Check_Response(supplier, response, foundlist):
            try:
                if response["Results"] == "Found":
                    foundlist.append(supplier)
            except Exception as e:
                pass

        suppliers = []

       # Checking the response of the scraped data from the two websites.
        response = self.scrap_Arrow(partnumber)
        Check_Response("arrow", response, suppliers)

        response = self.scrap_omron(partnumber)
        Check_Response("omron", response, suppliers)

        response = self.scrap_Rscomponents(partnumber)
        Check_Response("RS-components", response, suppliers)

        response = self.scrap_Maxim(partnumber)
        Check_Response("maxim", response, suppliers)

        response = self.scrap_Molex(partnumber)
        Check_Response("molex", response, suppliers)

        response = self.scrap_Wago(partnumber)
        Check_Response("wago", response, suppliers)

        response = self.scrap_Te(partnumber)
        Check_Response("Te", response, suppliers)

        response = self.scrap_Phoenix(partnumber)
        Check_Response("phoenix", response, suppliers)

        response = self.scrap_onsemi(partnumber)
        Check_Response("onsemi", response, suppliers)

        response = self.scrap_mouser(partnumber)
        Check_Response("mouser", response, suppliers)

        return suppliers


if __name__ == '__main__':
    scraper = Scrapper()
    print(scraper.find_Supplier("14"))
