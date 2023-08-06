def veh_values():
    """Doc string missing."""
    return {
        'PLATE_NO': 'PMN 961',
        'PLATE_ST': 'CA',
        'V_VIN': 'KMHTC6AE4FU221793',
        'V_MODEL_YR': '2015',
        'V_MAKECODE': 'TOYOTA',
        'V_MODEL': 'VELOSTER TURBORSPEC',
        'V_COLOR': 'WHITE',
        'V_TONE': 0,
        'V_STAGE': 0
    }


VEHICLE_FIELDS = {
    'IMPACT_1 C(2)': '',
    'IMPACT_2 C(30)': '',
    'DMG_MEMO C(10)': '',
    'DB_V_CODE C(7)': '',
    'PLATE_NO C(10)': veh_values()['PLATE_NO'],
    'PLATE_ST C(2)': veh_values()['PLATE_ST'],
    'V_VIN C(25)': veh_values()['V_VIN'],
    'V_COND C(2)': '',
    'V_PROD_DT C(4)': '',
    'V_MODEL_YR C(2)': veh_values()['V_MODEL_YR'][-2:],
    'V_MAKECODE C(12)': veh_values()['V_MAKECODE'],
    'V_MAKEDESC C(20)': '',
    'V_MODEL C(50)': veh_values()['V_MODEL'],
    'V_TYPE C(2)': '',
    'V_BSTYLE C(20)': '',
    'V_TRIMCODE C(20)': '',
    'TRIM_COLOR C(20)': '',
    'V_MLDGCODE C(20)': '',
    'V_ENGINE C(20)': '',
    'V_MILEAGE C(6)': '1',
    'V_OPTIONS C(10)': '',
    'V_COLOR C(20)': veh_values()['V_COLOR'],
    'V_TONE N(1,0)': veh_values()['V_TONE'],
    'V_STAGE N(1,0)': veh_values()['V_STAGE'],
    'PAINT_CD1 C(15)': '',
    'PAINT_CD2 C(15)': '',
    'PAINT_CD3 C(15)': '',
    'V_MEMO C(10)': ''
}
