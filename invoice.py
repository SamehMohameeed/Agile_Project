from abc import ABC, abstractmethod

FEE_PER_HOUR = 1200


class FeePolicy(ABC):
    """Common interface: every policy turns credit hours into a fee."""

    @abstractmethod
    def fee(self, hours):
        ...


class RegularPolicy(FeePolicy):
    RATE = FEE_PER_HOUR

    def fee(self, hours):
        return hours * self.RATE


class DiscountedPolicy(RegularPolicy):
    """Regular fee minus a percentage. Subclasses only set DISCOUNT."""

    DISCOUNT = 0.0

    def fee(self, hours):
        return super().fee(hours) * (1 - self.DISCOUNT)


class ScholarshipPolicy(DiscountedPolicy):
    DISCOUNT = 0.5


class SiblingPolicy(DiscountedPolicy):
    DISCOUNT = 0.25


class InternationalPolicy(FeePolicy):
    RATE = 2000
    SERVICE_FEE = 5000

    def fee(self, hours):
        return hours * self.RATE + self.SERVICE_FEE


POLICIES = {
    "regular": RegularPolicy(),
    "scholarship": ScholarshipPolicy(),
    "sibling": SiblingPolicy(),
    "international": InternationalPolicy(),
}


class FileWriter:
    def write(self, student_id, text):
        with open(f"invoice_{student_id}.txt", "w") as f:
            f.write(text)


def make_invoice(student, kind, writer=None):
    policy = POLICIES[kind]
    total = policy.fee(student.total_hours)
    text = f"Invoice for {student.student_id}: {int(total)} EGP"
    (writer or FileWriter()).write(student.student_id, text)
    return total
