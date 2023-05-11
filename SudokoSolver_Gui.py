import sys
import pandas as pd
from PyQt5.QtWidgets import (
 QWidget, QPushButton, QComboBox, QLabel,    
)

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

