import os
import pandas as pd
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog

class CSVFileHandler(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self.setText("Drag and drop a CSV file here or click 'Browse' to select a file.")
        self.setAlignment(Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.process_file(file_path)

    def process_file(self, file_path):
        df = pd.read_csv(file_path, encoding='utf-8', nrows=0)

        dialog = ColumnMappingDialog(df.columns)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            mapping = dialog.get_mapping()
            cleaned_df = clean_csv(file_path, mapping)
            if cleaned_df is not None:
                save_file(cleaned_df)

class ColumnMappingDialog(QtWidgets.QDialog):
    def __init__(self, columns, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select and Map CSV Columns")

        layout = QtWidgets.QVBoxLayout(self)

        self.column_comboboxes = {}

        translations = {
            'Падаан': 'Number',
            'Огноо': 'Date',
            'Харилцагч': 'Customer',
            'Бараа': 'Product',
            'Буцаалт': 'Return',
            'төлөх дүн': 'Payment',
            'Төлсөн': 'Paid',
            'Хөнгөлөлт': 'Discount'
        }

        for column in columns:
            combobox = QtWidgets.QComboBox()
            combobox.addItems(['Unmatched', *translations.keys()])
            layout.addWidget(QtWidgets.QLabel(f"{column}:"))
            layout.addWidget(combobox)

            self.column_comboboxes[column] = combobox

        buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout.addWidget(buttonBox)

    def get_mapping(self):
        return {column: combobox.currentText() for column, combobox in self.column_comboboxes.items()}

def clean_csv(file_path, mapping):
    df = pd.read_csv(file_path, encoding='utf-8')

    mapping = {k: v for k, v in mapping.items() if v != 'Unmatched'}
    df = df.rename(columns=mapping)

    for column in df.columns:
        if column not in mapping.values():
            df = df.drop(columns=column)

    return df

def save_file(dataframe):
    save_path, _ = QFileDialog.getSaveFileName(None, "Save CSV file", "", "CSV Files (*.csv)")
    if save_path:
        dataframe.to_csv(save_path, index=False)

def select_file():
    file_path, _ = QFileDialog.getOpenFileName(None, "Select CSV file", "", "CSV Files (*.csv)")
    if file_path:
        CSVFileHandler().process_file(file_path)

app = QtWidgets.QApplication([])

window = QtWidgets.QWidget()
window.setWindowTitle("CSV Borgotsoi File Exploration")

file_handler = CSVFileHandler()

button = QtWidgets.QPushButton("Browse")
button.clicked.connect(select_file)

layout = QtWidgets.QVBoxLayout(window)
layout.addWidget(file_handler)
layout.addWidget(button)

window.show()

app.exec_()
