import json
import uuid
import twint
import mmap
import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            map = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ)
            data=map.read().decode('utf-8')
            json_data=json.loads(data)
            f.close()
        return json_data
    except Exception as e:
        print(e)


unemploymentRateData = read_json_file("JSON/unemployment_rate.json")
unemploymentRateData = unemploymentRateData["features"]
format_unemploymentRateData = {}
for each in unemploymentRateData:
    rates = []
    for key in each["properties"]:
        if("mar_" in key):
            year = key.replace("mar_","")
            rates.append({"year":int(year),"month":3,"value":each["properties"][key]})
        elif("jun_" in key):
            year = key.replace("jun_","")
            rates.append({"year":int(year),"month":6,"value":each["properties"][key]})
        elif("sep_" in key):
            year = key.replace("sep_","")
            rates.append({"year":int(year),"month":9,"value":each["properties"][key]})
        elif("dec_" in key):
            year = key.replace("dec_","")
            rates.append({"year":int(year),"month":12,"value":each["properties"][key]})
    for index in range(len(rates)):
        if(index > 0):
            for i in range(index):
                if(rates[index]["year"]<rates[i]["year"]):
                    rates[i],rates[index] = rates[index], rates[i]
                elif(rates[index]["year"]==rates[i]["year"]):
                    if(rates[index]["month"]<rates[i]["month"]):
                        rates[i],rates[index] = rates[index], rates[i]

    format_unemploymentRateData[each["properties"]["sa2_main11"]] = rates

def unemploymentrate(sa2_main11):
    if (sa2_main11 in format_unemploymentRateData.keys()):
        result = {"data":format_unemploymentRateData[str(sa2_main11)],"isSuccess":True}
    else:
        result = {"data":None,"message":"no data","isSuccess":True}
    return result

education_backgroud = read_json_file("JSON/education_backgroud.json")["features"]
def educationBackgroud():
    data = []
    for each in education_backgroud:
        if(each["properties"]["gcc_name16"] == "Greater Melbourne"):
            data.append({"cityName":"Melbourne","count":(each["properties"]["p_y12e_tot"]/4936000)})
        elif(each["properties"]["gcc_name16"] == "Greater Sydney"):
            data.append({"cityName":"Sydney","count":(each["properties"]["p_y12e_tot"]/5230000)})
        elif(each["properties"]["gcc_name16"] == "Greater Brisbane"):
            data.append({"cityName":"Brisbane","count":(each["properties"]["p_y12e_tot"]/2280000)})
        elif(each["properties"]["gcc_name16"] == "Greater Adelaide"):
            data.append({"cityName":"Adelaide","count":(each["properties"]["p_y12e_tot"]/1316779)})
        elif(each["properties"]["gcc_name16"] == "Greater Perth"):
            data.append({"cityName":"Perth","count":(each["properties"]["p_y12e_tot"]/1985000)})
    return {"isSuccess":True,"data":data}

industry_of_employment_by_occupation = read_json_file("JSON/industry_of_employment_by_occupation.json")["features"]
industry_of_employment_by_occupation_metadata = read_json_file("JSON/industry_of_employment_by_occupation_metadata.json")["selectedAttributes"]
keyToTitle = {}
for each in industry_of_employment_by_occupation_metadata:
    if("tot" in each["name"]):
        keyToTitle[each["name"]] = each["title"]
def industryOfEmploymentByOccupation():
    cityNames = ["Greater Sydney","Greater Melbourne","Greater Brisbane","Greater Adelaide","Greater Perth"]
    data = {}
    for each in industry_of_employment_by_occupation:
        city = {}
        for item in each["properties"]:
            if("tot" in item):
                city[keyToTitle[item].replace(" Total","")] = each["properties"][item]
        if(each["properties"]["gcc_name16"] in cityNames):
            data[each["properties"]["gcc_name16"]]=city
    return {"isSuccess":True,"data":data}

centrelink_file =  read_json_file("JSON/centrelink.json")["features"]
centrelink_data = {}
for each in centrelink_file:
    centrelink_data[each['properties']['gcc_name16']] = {
        'slct_gov_pnsn_alwn_age_pension_centrelink_num': each['properties']['slct_gov_pnsn_alwn_age_pension_centrelink_num'],
        'slct_gov_pnsn_alwn_fam_tax_bft_num': each['properties']['slct_gov_pnsn_alwn_fam_tax_bft_num'],
        'slct_gov_pnsn_alwn_fam_tax_bft_b_num': each['properties']['slct_gov_pnsn_alwn_fam_tax_bft_b_num']
        }
def centrelink():
    cityNames = ["Greater Sydney","Greater Melbourne","Greater Brisbane","Greater Adelaide","Greater Perth"]
    data = {}
    for each in cityNames:
        data[each.replace('Greater ','')] = {
            'Centrelink Num':centrelink_data[each]['slct_gov_pnsn_alwn_age_pension_centrelink_num'],
            'Family Tax Benefit A':centrelink_data[each]['slct_gov_pnsn_alwn_fam_tax_bft_num'],
            'Family Tax Benefit B':centrelink_data[each]['slct_gov_pnsn_alwn_fam_tax_bft_b_num']
            }
    return {'isSuccess':True,'data':data}

social_benifit =  read_json_file("JSON/social_benefit.json")["features"]
social_benifit_data = {}
for each in social_benifit:
    social_benifit_data[each['properties']['gccsa_name']] = {
        'sgpa_tot_fam_tax_benf_recip': each['properties']['sgpa_tot_fam_tax_benf_recip'],
        'sgpa_family_tax_benefit_a': each['properties']['sgpa_family_tax_benefit_a'],
        'sgpa_family_tax_benefit_b': each['properties']['sgpa_family_tax_benefit_b']
        }
def socialBenifit():
    cityNames = [["Greater Sydney",1247047],["Greater Melbourne",1161643],["Greater Brisbane",591505],["Greater Adelaide",343888],["Greater Perth",515328]]
    data = {}
    for each in cityNames:
        data[each[0].replace('Greater ','')] = {
            'Family Tax Benefit A and B':social_benifit_data[each[0]]['sgpa_tot_fam_tax_benf_recip']/each[1],
            'Family Tax Benefit A':social_benifit_data[each[0]]['sgpa_family_tax_benefit_a']/each[1],
            'Family Tax Benefit B':social_benifit_data[each[0]]['sgpa_family_tax_benefit_b']/each[1]
            }
    return {'isSuccess':True,'data':data}