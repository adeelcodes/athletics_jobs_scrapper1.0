from typing import Dict, List, NoReturn

from parsing.settings import service, GOOGLE_SPREADSHEET_ID


def get_list_data_from_dict(data: Dict) -> List[str]:
    """
    Return list data from dict values.
    :param data:
    :return:
    """
    result_list = []
    for item in data.values():
        if isinstance(item, str):
            result_list.append(item)
        else:
            result_list.append('')
    return result_list


def append_row_in_google_sheet(data: List[List[str]], range: str) -> NoReturn:
    """
    Insert new data into google sheet
    :param data: For example
    [
        ["sample1", "sample2", "sample3"],
        ["sample12", "sample22", "sample32"],
    ]
    :param range: The A1 notation of a range to search for a logical table of data.
            Values will be appended after the last row of the table.
    :return:
    """

    # How the input data should be interpreted.
    # value_input_option = 'RAW'
    value_input_option = 'USER_ENTERED'

    # How the input data should be inserted.
    insert_data_option = 'INSERT_ROWS'

    value_range_body = {
        "values": data
    }

    request = service.spreadsheets().values().append(
        spreadsheetId=GOOGLE_SPREADSHEET_ID,
        range=range,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body)
    response = request.execute()
