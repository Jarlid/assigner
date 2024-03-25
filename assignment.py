from random import randrange


class _ServiceException(Exception):
    pass


class Assignment:
    def __init__(self, works: list[str], reviewers: list[(str, int)], reviewers_per_work: int):
        self._works = works
        self._reviewers = reviewers
        self._reviewers_per_work = reviewers_per_work

        while True:
            try:
                temp_reviewer_nums = [r[1] for r in reviewers]
                self._assignment = []

                for _work in self._works:
                    work_reviewers = set()
                    generator_num = sum(temp_reviewer_nums)

                    while len(work_reviewers) < reviewers_per_work:
                        if generator_num <= 0:
                            raise _ServiceException
                        rand_num = randrange(generator_num)

                        for i, reviewer_num in enumerate(temp_reviewer_nums):
                            if i in work_reviewers:
                                continue

                            rand_num -= reviewer_num

                            if rand_num < 0:
                                generator_num -= reviewer_num
                                temp_reviewer_nums[i] -= 1
                                work_reviewers.add(i)
                                break

                    self._assignment.append(work_reviewers)

            except _ServiceException:
                continue

            else:
                break

    def get_sheet_size(self):
        return len(self._assignment), self._reviewers_per_work + 1

    def put_in_worksheet(self, worksheet):
        for row_i, work_reviewers in enumerate(self._assignment):
            worksheet.update_cell(row_i + 1, 1, self._works[row_i])

            for col_i, reviewer_i in enumerate(work_reviewers):
                worksheet.update_cell(row_i + 1, col_i + 2, self._reviewers[reviewer_i][0])
