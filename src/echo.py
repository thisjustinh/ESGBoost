from json.decoder import JSONDecodeError
import requests
import re
import pandas as pd


def call_echo(name, zip_code):
    # GET Registry ID
    frs_url = f"https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?zip_code={zip_code}&facility_name={name}&output=JSON"
    # Handle EPA JSON syntax errors
    try:
        r = requests.get(frs_url).json()
    except JSONDecodeError:
        return None
    id = None
    
    # If multiple results, find the one whose name matches exactly
    for d in r['Results']['FRSFacility']:
        if d['FacilityName'] == name:
            id = d['RegistryId']
            break
    # If exact match not found, use first result
    if id is None:
        try:
            id = r['Results']['FRSFacility'][0]['RegistryId']
            print(id)
        except IndexError:
            return None

    # POST ECHO data
    echo_url = "https://echodata.epa.gov/echo/dfr_rest_services.get_dfr"
    post_head = {
        'output': 'JSON',
        'p_id': id,
    }
    r = requests.post(echo_url, data=post_head).json()

    try:
        # Demographics
        demographics = r['Results']['Demographics']
        dem_factors = [
            "PercentMinority", "Less9thGrade", "Grades9to12", "HSDiploma", "SomeCollege", "BSBA", "IncomeLess15k", "Income15to25k","Income25to50k","Income50to75k","Income75kPlus"
        ]
        demographics = {key: demographics[key] for key in dem_factors}

        # Air Quality Pollutants
        # air_quality = r['Results']['AirQualityNAAs']['AirQualityNAA']
        # maint_pollutants = []
        # na_pollutants = []
        # for d in air_quality:
        #     if d['WithinMaintStatusArea'] == 'Yes':
        #         maint_pollutants.append(d['Pollutant'])
        #     if d['WithinNAStatusArea'] == 'Yes':
        #         na_pollutants.append(d['Pollutant'])
        # maint_pollutants = ','.join(maint_pollutants)
        # na_pollutants = ','.join(na_pollutants)

        # # Number of Non-Compliance and Significant Non-Compliance Checks
        # qtrs_in_nc = r['Results']['EnforcementComplianceSummaries']['Summaries'][0]['QtrsInNC']
        # qtrs_in_snc = r['Results']['EnforcementComplianceSummaries']['Summaries'][0]['QtrsInSNC']

        # # Start and End dates for Compliance
        # start = r['Results']['ComplianceSummary']['ProgramDates'][0]['StartDate']
        # end = r['Results']['ComplianceSummary']['ProgramDates'][0]['EndDate']

        # Environmental Justice Screen Indexes
        ej = r['Results']['EJScreenIndexes']
        ej.pop('RegistryID')
        ej.pop('Over80Count')
    except KeyError:
        return None

    # echo = [start, end, qtrs_in_nc, qtrs_in_snc, na_pollutants, maint_pollutants]
    echo = list(demographics.values())
    echo.extend(list(ej.values()))

    return echo


if __name__ == '__main__':
    echo = []
    skipped = []
    info = pd.read_csv('src/zip-copy.csv')

    # Go through each company to get ECHO data
    for index, row in info.iterrows():
        name = re.sub(r'[!,*)@#%(&$_?^]', '', row['longName'])
        print(name)
        row_echo = call_echo(name, row['zip'])
        if row_echo is None:
            skipped.append(row['ticker'])
            continue
        new_row = [row['ticker']]
        new_row.extend(row_echo)
        echo.append(new_row)
        print(row['ticker'])

    df = pd.DataFrame(echo, columns=['ticker',
                                    'minority_pct',
                                    'primary_school',
                                    'high_school',
                                    'hs_diploma',
                                    'some_college',
                                    'bsba',
                                    'income_l15',
                                    'income_15_25',
                                    'income_25_50',
                                    'income_50_75',
                                    'income_p75',
                                    'pm25',
                                    'ozone',
                                    'nata_dieselpm',
                                    'nata_cancerrisk',
                                    'nata_resphi',
                                    'traffic_prox',
                                    'lead_paint',
                                    'rmp_prox',
                                    'superfund_prox',
                                    'hazardwaste_prox',
                                    'waterdischarge_prox'])
    df.to_csv('echo.csv')
    print(df)
