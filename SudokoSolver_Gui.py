import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QComboBox, QLabel, QFileDialog,
    QMessageBox, QVBoxLayout, QHBoxLayout, QSizePolicy
)
from functions import *


class SolverGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window title and size
        self.setWindowTitle('Solver GUI')
        self.setGeometry(100, 100, 400, 200)

        # Create label and button to import file
        self.lbl_import = QLabel('Import your Excel file:', self)
        self.btn_import = QPushButton('Browse', self)
        self.btn_import.clicked.connect(self.import_file)

        # Create dropdown list and label to select algorithm
        self.lbl_algorithm = QLabel('Select Algorithm:', self)
        self.cb_algorithm = QComboBox(self)
        self.cb_algorithm.addItems(['Backtracking', 'Depth Limited Search', 'Breadth First Search'])

        # Create button to solve problem
        self.btn_solve = QPushButton('Solve', self)
        self.btn_solve.clicked.connect(self.solve_problem)

        # Create layout for file import widgets
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.lbl_import)
        file_layout.addWidget(self.btn_import)

        # Create layout for algorithm selection widgets
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(self.lbl_algorithm)
        algorithm_layout.addWidget(self.cb_algorithm)

        # Create layout for solve button
        solve_layout = QHBoxLayout()
        solve_layout.addWidget(self.btn_solve)

        # Create main layout and add sub-layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(file_layout)
        main_layout.addLayout(algorithm_layout)
        main_layout.addLayout(solve_layout)

        # Set main layout and add spacer to bottom
        self.setLayout(main_layout)
        spacer = QLabel('', self)
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(spacer)

    def import_file(self):
        # Open file dialog and get selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'Excel Files (*.xlsx)')
        if file_path:
            # Call function to process the file
            self.data = self.process_file(file_path)
            try:
                if self.data['error_code']:
                    QMessageBox.information(self, 'ERROR!',
                                            f'File {file_path} was not imported successfully!\nError Code : {self.data["error_code"]}')
            except:
                QMessageBox.information(self, 'SUCCESS!', f'File {file_path} was imported successfully!')
                print(self.data)  # contains matrix with numbers

    def process_file(self, file_path):
        # Read Excel file using pandas
        data = read_table(file_path)
        # Add code to process the file as required
        return data

    def solve_problem(self):
        # Get selected algorithm from dropdown list
        algorithm = self.cb_algorithm.currentText()

        # Check if a file has been imported before solving the problem
        if not hasattr(self, 'data'):
            QMessageBox.warning(self, 'No File Found',
                                'Please import an Excel file before attempting to solve the problem.')
            return

        # Add code to solve the problem using selected algorithm
        # Create Excel file with results
        result_file_path = 'results.xlsx'
        results = pd.DataFrame({'Algorithm': [algorithm], 'Result': ['TODO']})
        results.to_excel(result_file_path, index=False)
        print(f'Results saved to {result_file_path}')

        # Display a success message
        QMessageBox.information(self, 'Success!', f'Results saved to {result_file_path}!')


if __name__ == '__main__':
    # Create application and window
    app = QApplication(sys.argv)
    solver_gui = SolverGUI()
    solver_gui.show()
    # Run application event
    app.exec_()
