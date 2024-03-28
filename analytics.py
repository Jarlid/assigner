class ReviewerVarianceInfo:
    def __init__(self):
        self._deviations = []

    def add(self, deviation: float):
        self._deviations.append(deviation)

    @property
    def num(self) -> float:
        return len(self._deviations)

    @property
    def mean_deviation(self) -> float:
        return sum(self._deviations) / len(self._deviations)

    @property
    def mean_modular_deviation(self) -> float:
        return sum(map(abs, self._deviations)) / len(self._deviations)


def analytics(worksheet_data):
    reviewer_dict = dict()

    for w in range(0, len(worksheet_data), 2):
        reviewer_indexes = [r for r in range(1, len(worksheet_data[w])) if worksheet_data[w][r] != '']

        w_sum = 0
        for r in reviewer_indexes:
            w_sum += float(worksheet_data[w + 1][r])

        for r in reviewer_indexes:
            reviewer = worksheet_data[w][r]

            if reviewer not in reviewer_dict:
                reviewer_dict[reviewer] = ReviewerVarianceInfo()

            reviewer_dict[reviewer].add(float(worksheet_data[w + 1][r]) - w_sum / len(reviewer_indexes))

    return [["Reviewer:", "Review num:", "Mean deviation:", "Mean modular deviation:"]] + \
        [[reviewer, reviewer_dict[reviewer].num, reviewer_dict[reviewer].mean_deviation,
          reviewer_dict[reviewer].mean_modular_deviation] for reviewer in reviewer_dict]