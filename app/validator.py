from abc import ABC, abstractmethod

DNA_LETTERS = "ACGT"


class ValidationError(Exception):
    pass


class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, dna: list[str]) -> bool:
        pass


class LengthValidationStrategy(ValidationStrategy):
    def validate(self, dna: list[str]) -> bool:
        if not all(len(sequence) == len(dna) for sequence in dna):
            raise ValidationError(
                "All DNA sequences must be of the same length."
            )
        return True


class CharacterValidationStrategy(ValidationStrategy):
    def validate(self, dna: list[str]) -> bool:
        if not all(
            char in DNA_LETTERS for sequence in dna for char in sequence
        ):
            raise ValidationError(
                "DNA sequences should contain valid "
                f"characters ({DNA_LETTERS})"
            )
        return True


class Validator:
    def __init__(self):
        self.strategies = [
            LengthValidationStrategy(),
            CharacterValidationStrategy(),
        ]

    def validate(self, dna: list[str]) -> bool:
        try:
            return all(strategy.validate(dna) for strategy in self.strategies)
        except ValidationError as e:
            raise Exception(f"Validation error: {e}")
