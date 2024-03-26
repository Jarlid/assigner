from flow import get_flow


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

    def put_in_worksheet(self, worksheet):
        for row_i, work_reviewers in enumerate(self._assignment):
            worksheet.update_cell(row_i + 1, 1, self._works[row_i])

            for col_i, reviewer_i in enumerate(work_reviewers):
                worksheet.update_cell(row_i + 1, col_i + 2, self._reviewers[reviewer_i][0])
