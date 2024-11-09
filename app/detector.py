from abc import ABC, abstractmethod


class DetectionStrategy(ABC):
    @abstractmethod
    def detect(self, dna: list[str], i: int, j: int, n: int) -> bool:
        pass


class HorizontalDetection(DetectionStrategy):
    def detect(self, dna: list[str], i: int, j: int, n: int) -> bool:
        return (
            j + 3 < n
            and dna[i][j] == dna[i][j + 1] == dna[i][j + 2] == dna[i][j + 3]
        )


class VerticalDetection(DetectionStrategy):
    def detect(self, dna: list[str], i: int, j: int, n: int) -> bool:
        return (
            i + 3 < n
            and dna[i][j] == dna[i + 1][j] == dna[i + 2][j] == dna[i + 3][j]
        )


class DiagonalDetection(DetectionStrategy):
    def detect(self, dna: list[str], i: int, j: int, n: int) -> bool:
        return (
            i + 3 < n
            and j + 3 < n
            and dna[i][j]
            == dna[i + 1][j + 1]
            == dna[i + 2][j + 2]
            == dna[i + 3][j + 3]
        )


class Detector:
    def __init__(self):
        self.strategies = [
            HorizontalDetection(),
            VerticalDetection(),
            DiagonalDetection(),
        ]

    def detect(self, dna: list[str]) -> bool:
        n = len(dna)
        sequences_number = 0
        for i in range(n):
            for j in range(n):
                for strategy in self.strategies:
                    if strategy.detect(dna, i, j, n):
                        sequences_number += 1

        return sequences_number > 1
