from PySide6.QtCore import Qt, QAbstractTableModel

from crypto_core.objects import Transaction


class TransactionTableModel(QAbstractTableModel):
    """Model to display transactions data in a table"""

    def __init__(self, transactions: list[Transaction] = list()):
        super().__init__()
        self.transactions = sorted(transactions)
        self.columns = (
            "Currency send",
            "Amount send",
            "Currency received",
            "Amount received"
        )

    def rowCount(self, parent) -> int:
        return len(self.transactions)

    def columnCount(self, parent) -> int:
        return len(self.columns)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columns[section]

        elif role == Qt.TextAlignmentRole and orientation == Qt.Horizontal:
            return Qt.AlignCenter

        elif role == Qt.DisplayRole and orientation == Qt.Vertical:
            return str(self.transactions[section].date)

        elif role == Qt.TextAlignmentRole and orientation == Qt.Vertical:
            return Qt.AlignLeft | Qt.AlignVCenter

    def data(self, index, role):
        transaction = self.transactions[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return transaction.currency_send.name

            elif index.column() == 1:
                return transaction.amount_send

            elif index.column() == 2:
                return transaction.currency_received.name

            elif index.column() == 3:
                return transaction.amount_received

