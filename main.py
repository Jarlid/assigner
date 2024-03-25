from sys import argv

import gspread

from assignment import Assignment

REVIEWERS_PER_WORK = 2


def processing_base(url: str, credentials_filename: str):
    gc = gspread.service_account(filename=credentials_filename)
    spreadsheet = gc.open_by_url(url)

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
        worksheet = spreadsheet.get_worksheet(2).duplicate(insert_sheet_index=3, new_sheet_name="Review scores")

        worksheet.append_row(["Scores:"])
        for row_i in range(worksheet.row_count - 1, 1, -1):
            worksheet.insert_row(["Scores:"], index=row_i)

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

        return

    else:
        exit(123822)  # TODO


if __name__ == "__main__":
    # argv[1] -- url google-таблицы.
    # argv[2] -- путь к файлу с данными сервис-аккаунта.
    processing_base(argv[1], argv[2])
