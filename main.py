from sys import argv

import gspread
from gspread.utils import rowcol_to_a1

from assignment import Assignment
from analytics import analytics

REVIEWERS_PER_WORK = 2


def processing_base(url: str, credentials_filename: str):
    gc = gspread.service_account(filename=credentials_filename)
    spreadsheet = gc.open_by_url(url)

    if len(spreadsheet.worksheets()) < 2:
        exit(347862387)  # TODO?

    if len(spreadsheet.worksheets()) == 2:
        works = []
        for row in spreadsheet.get_worksheet(0).get_all_values():
            works.append(row[0])

        reviewers = []
        for row in spreadsheet.get_worksheet(1).get_all_values():
            reviewers.append((row[0], int(row[1])))

        assignment = Assignment(works, reviewers, REVIEWERS_PER_WORK)
        assignment_sheet = spreadsheet.add_worksheet("Assignment", *assignment.get_sheet_size())
        assignment.put_in_worksheet(assignment_sheet)

    if len(spreadsheet.worksheets()) == 3:
        new_values = []
        max_length = 1

        for old_value in spreadsheet.get_worksheet(2).get_all_values():
            new_values.append(old_value)
            new_values.append(["Score:"])

            max_length = max(max_length, len(old_value))

        scores_worksheet = spreadsheet.add_worksheet("Review scores", len(new_values), max_length)
        scores_worksheet.update(range_name=f"A1:{rowcol_to_a1(len(new_values), max_length)}", values=new_values)

        """
        for row_i in range(2, worksheet.row_count + 1, 2):
            worksheet.format(f"A{row_i}", {
                "textFormat": {
                    "foregroundColor": {
                        "red": 0.5,
                        "green": 0.5,
                        "blue": 0.5
                    }
                }
            })
        """

        return

    else:
        scores_worksheet_data = spreadsheet.get_worksheet(3).get_all_values()

        to_sheet = analytics(scores_worksheet_data)

        analytics_worksheet = spreadsheet.add_worksheet("Analytics", len(to_sheet), len(to_sheet[0]))
        analytics_worksheet.update(range_name=f"A1:{rowcol_to_a1(len(to_sheet), len(to_sheet[0]))}", values=to_sheet)

        return


if __name__ == "__main__":
    # argv[1] -- url google-таблицы.
    # argv[2] -- путь к файлу с данными сервис-аккаунта.
    processing_base(argv[1], argv[2])
