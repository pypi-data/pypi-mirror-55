from typing import Optional

from sqltask.base.table import BaseOutputRow

class BaseRowTarget:
    """
    Base class for for output rows. A RowTarget offers instances of OutputRow that
    can be mutated and finally appended to the RowTarget, which ultimately are output
    to whichever sink it implements.
    """
    def __init__(
            self,
            name: Optional[str] = None,
            timestamp_column_name: Optional[str] = None,
    ):
        self.name = name
        self.timestamp_column_name = timestamp_column_name

    def get_new_row(self) -> "BaseOutputRow":
        """
        Get a new row intended to be added to the table.
        """
        output_row = BaseOutputRow(self)
        if self.timestamp_column_name:
            output_row[self.timestamp_column_name] = datetime.utcnow()
        return output_row
