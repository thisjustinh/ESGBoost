import requests
import pandas as pd

def call_echo(name, zip_code):
    # GET Registry ID
    frs_url = f"https://ofmpub.epa.gov/frs_public2/frs_rest_services.get_facilities?zip_code={zip_code}&facility_name={name}&output=JSON"
    r = requests.get(frs_url).json()
    id = r['Results']['FRSFacility'][0]['RegistryId']

    # POST ECHO data
    echo_url = "https://echodata.epa.gov/echo/dfr_rest_services.get_dfr"
    post_head = {
        'output': 'JSON',
        'p_id': id,
    }
    r = requests.post(echo_url, data=post_head).json()

    # Demographics
    demographics = r['Results']['Demographics']
    dem_factors = [
        "PercentBelowPovertyLevel", "PercentPeopleOfColor", "Less9thGrade", "Grades9to12", "HSDiploma", "SomeCollege", "BSBA", "IncomeLess15k", "Income15to25k","Income25to50k","Income50to75k","Income75kPlus"
    ]
    demographics = {key: demographics[key] for key in dem_factors}

    # Air Quality Pollutants
    air_quality = r['Results']['AirQualityNAAs']['AirQualityNAA']
    maint_pollutants = []
    na_pollutants = []
    for d in air_quality:
        if d['WithinMaintStatusArea'] == 'Yes':
            maint_pollutants.append(d['Pollutant'])
        if d['WithinNAStatusArea'] == 'Yes':
            na_pollutants.append(d['Pollutant'])
    maint_pollutants = ','.join(maint_pollutants)
    na_pollutants = ','.join(na_pollutants)

    # Number of Non-Compliance and Significant Non-Compliance Checks
    qtrs_in_nc = r['Results']['EnforcementComplianceSummaries']['Summaries'][0]['QtrsInNC']
    qtrs_in_snc = r['Results']['EnforcementComplianceSummaries']['Summaries'][0]['QtrsInSNC']

    # Start and End dates for Compliance
    start = r['Results']['ComplianceSummary']['ProgramDates'][0]['StartDate']
    end = r['Results']['ComplianceSummary']['ProgramDates'][0]['EndDate']

    # Environmental Justice Screen Indexes
    ej = r['Results']['EJScreenIndexes']
    ej.pop('RegistryID')
    ej.pop('Over80Count')

    echo = [start, end, qtrs_in_nc, qtrs_in_snc, na_pollutants, maint_pollutants]
    echo.extend(list(demographics.values()))
    echo.extend(list(ej.values()))

    return echo


if __name__ == '__main__':
    echo = []
    # TODO: Get CSV of zip codes and names, and modify the following as necessary
    info = pd.read_csv('info.csv')

    # Go through each company to get ECHO data
    for index, row in info.iterrows():
        row_echo = call_echo(row['name'], row['zip_code'])
        print(row_echo)
        echo.append(row_echo)

    df = pd.DataFrame(echo, columns=['start_date',
                                    'end_date',
                                    'qtrs_in_nc',
                                    'qtrs_in_snc',
                                    'na_pollutants',
                                    'maint_pollutants',
                                    'poverty_pct',
                                    'poc_pct',
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
