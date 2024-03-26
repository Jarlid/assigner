from flow import get_flow

from gspread.utils import rowcol_to_a1


class Assignment:
    class InsufficientReviewers(Exception):
        pass

    def __init__(self, works: list[str], reviewers: list[(str, int)], reviewers_per_work: int):
        self._works = works
        self._reviewers = reviewers
        self._reviewers_per_work = reviewers_per_work

        works_part_size = 1 + len(works)
        graph_size = works_part_size + len(reviewers) + 1
        graph = [[0 for _ in range(graph_size)] for _ in range(graph_size)]

        for w in range(1, works_part_size):
            graph[0][w] = reviewers_per_work

            for r in range(works_part_size, graph_size - 1):
                graph[w][r] = 1

        for r in range(works_part_size, graph_size - 1):
            graph[r][graph_size - 1] = reviewers[r - works_part_size][1]

        flow, graph = get_flow(graph, 0, graph_size - 1)

        if flow < reviewers_per_work * len(works):
            raise Assignment.InsufficientReviewers()

        self._assignment = []
        for w in range(1, works_part_size):
            work_reviewers = set()

            for r in range(works_part_size, graph_size - 1):
                if graph[r][w] == 1:
                    work_reviewers.add(r - works_part_size)

            self._assignment.append(work_reviewers)

    def get_sheet_size(self):
        return len(self._assignment), self._reviewers_per_work + 1

    def get_reviewer_name(self, reviewer_i: int) -> str:
        return self._reviewers[reviewer_i][0]

    def put_in_worksheet(self, worksheet):
        rows, cols = self.get_sheet_size()
        end = rowcol_to_a1(rows, cols)

        worksheet.update(f"A1:{end}", [[self._works[i]] +
                                       list(map(self.get_reviewer_name, self._assignment[i])) for i in range(rows)])
