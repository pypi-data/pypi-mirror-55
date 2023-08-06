import dbf


def env_values():
    """Doc string missing."""
    return {
        'UNQFILE_ID': '',  # claim.id
        'ESTFILE_ID': '',  # claim.id
        'DB_DATE': dbf.Date(1979, 9, 13),
        'TRANS_TYPE': 'A',
        'STATUS': None,
        'CREATE_DT': dbf.Date(1979, 9, 13),
        'TRANSMT_DT': dbf.Date(1979, 9, 13),
        'INCL_ADMIN': True,
        'INCL_VEH': True,
        'INCL_EST': False,
        'INCL_PROFL': False,
        'INCL_TOTAL': False,
        'INCL_VENDR': False,
        'EMS_VER': '2.0'
    }


ENVIRONMENT_FIELDS = {
    'EST_SYSTEM C(1)': '',
    'SW_VERSION C(10)': '',
    'DB_VERSION C(12)': '',
    'DB_DATE D': env_values()['DB_DATE'],
    'UNQFILE_ID C(8)': env_values()['UNQFILE_ID'],
    'RO_ID C(8)': '',
    'ESTFILE_ID C(38)': env_values()['ESTFILE_ID'],
    'SUPP_NO C(3)': '',
    'EST_CTRY C(3)': '',
    'TOP_SECRET C(80)': '',
    'H_TRANS_ID C(9)': '',
    'H_CTRL_NO C(9)': '',
    'TRANS_TYPE C(1)': 'A',
    'STATUS L': env_values()['STATUS'],
    'CREATE_DT D': env_values()['CREATE_DT'],
    'CREATE_TM C(6)': '',
    'TRANSMT_DT D': env_values()['TRANSMT_DT'],
    'TRANSMT_TM C(6)': '',
    'INCL_ADMIN L': env_values()['INCL_ADMIN'],
    'INCL_VEH L': env_values()['INCL_VEH'],
    'INCL_EST L': env_values()['INCL_EST'],
    'INCL_PROFL L': env_values()['INCL_PROFL'],
    'INCL_TOTAL L': env_values()['INCL_TOTAL'],
    'INCL_VENDR L': env_values()['INCL_VENDR'],
    'EMS_VER C(5)': env_values()['EMS_VER']
}
