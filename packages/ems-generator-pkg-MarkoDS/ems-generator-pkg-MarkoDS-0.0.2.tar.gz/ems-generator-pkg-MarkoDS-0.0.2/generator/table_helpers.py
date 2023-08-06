from .structure import (ADDRESS_1_FIELDS, ADDRESS_2_FIELDS, ENVIRONMENT_FIELDS,
                        VEHICLE_FIELDS)


def table_structure(ems_type: str) -> dict:
    """
    Return a structure with field names and default falues for given ems_type.

    :param ems_type:  String, '.ad1', '.ad2', '.veh', '.env'
    :return: Dict with table structure if structure for received
             ems_type is defined. {'INS_CO_NM': 'ACD', 'INS_CTRY': 'USA' ...}
    """
    structures = {
        '.ad1': ADDRESS_1_FIELDS,
        '.ad2': ADDRESS_2_FIELDS,
        '.veh': VEHICLE_FIELDS,
        '.env': ENVIRONMENT_FIELDS
    }

    try:
        return structures[ems_type]
    except KeyError:
        return 'Structure does not exists!'


def table_field_specs(structure: dict) -> list:
    """
    Return a list of field specifications for given structure.

    :param structure:  Dictionary, {'INS_ST C(1)': '', 'SUPP_NO C(10)': '' ...}
    :return: List of strings. Each string represent field specifiaction.
            ['INS_ST C(1)', 'SUPP_NO C(10)', ...]

    """
    return [key for key, value in structure.items()]


def table_default_values(structure: dict) -> list:
    """
    Return a list of default values for given structure.

    :param structure:  Dictionary, {'OWNR_FN': 'JOHN', 'OWNR_LN': 'DOE' ...}
    :return: List of strings. Each string represent a value.
            ['JOHN', 'DOE', ...]

    """
    return [value for key, value in structure.items()]


def table_name(ems_type: str, est_software: str, claim={}) -> str:
    """
    Return table name for given based on given est_software.

    Calls mitchell_table_name() or default_table_name().

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param est_software: String, 'M', 'C', 'A'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: mitchell_table_name() or default_table_name()
    """
    names = {
        'M': mitchell_table_name(ems_type, claim['CLAIM_NUMBER']),
        'C': default_table_name(ems_type, claim['CLAIM_NUMBER']),
        'A': default_table_name(ems_type, claim['CLAIM_NUMBER'])
    }

    return names[est_software]


def mitchell_table_name(ems_type: str, claim={}) -> str:
    """
    Construct a table name for mitchell with given claim and ems_type.

    Adds 'a' or 'b' or 'v' to file names based on receivied ems_type.

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: claim['CLAIM_NUMBER'] + 'a' or 'b' or 'v' + ems_type, 'TEST.veh'
    """
    names = {
        '.ad1': claim['CLAIM_NUMBER'] + 'a',
        '.ad2': claim['CLAIM_NUMBER'] + 'b',
        '.veh': claim['CLAIM_NUMBER'] + 'v',
        '.env': claim['CLAIM_NUMBER']
    }

    return names[ems_type] + ems_type


def default_table_name(ems_type: str, claim={}) -> str:
    """
    Construct a default name for table with given claim and ems_type.

    :param ems_type: String, '.ad1', '.ad2', '.veh', '.env'
    :param claim: Dictionary, {'CLAIM_NUMBER': 'TEST', 'OWNR_LN': 'DOE' ...}
    :return: claim['CLAIM_NUMBER'] + ems_type, 'TEST.veh'
    """
    return claim['CLAIM_NUMBER'] + ems_type
