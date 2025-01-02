import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QListWidget, QLabel, QCheckBox, QSpinBox, QComboBox, QFileDialog, 
    QMessageBox, QLineEdit, QVBoxLayout, QHBoxLayout
)
from PyQt5 import uic
from run_calculations import Calculations
from create_potcar import build_potcar  # Assuming you have a build_potcar function


class SplashWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration Window")
        self.resize(400, 300)

        # Layouts
        main_layout = QVBoxLayout()

        # Widgets
        self.info_label = QLabel("Enter the configuration details before starting:")

        # Allocation Type Dropdown
        self.allocation_label = QLabel("Allocation Type:")
        self.allocation_dropdown = QComboBox()
        self.allocation_dropdown.addItems(["cda090008", "cda090008-gpu", "cis220051", "cis220051-gpu", "med240015"])

        # Queue/Partition Dropdown
        self.queue_label = QLabel("Queue/Partition:")
        self.queue_dropdown = QComboBox()
        self.queue_dropdown.addItems(["wholenode", "shared", "gpu"])

        # Number of Nodes
        self.nodes_label = QLabel("Number of Nodes:")
        self.nodes_spinbox = QSpinBox()
        self.nodes_spinbox.setRange(1, 100)  # Adjust range as needed

        # Number of Tasks
        self.tasks_label = QLabel("Number of Tasks:")
        self.tasks_spinbox = QSpinBox()
        self.tasks_spinbox.setRange(1, 1000)  # Adjust range as needed

        # Time Requested
        self.time_label = QLabel("Time Requested (hours):")
        self.time_spinbox = QSpinBox()
        self.time_spinbox.setRange(1, 72)  # Adjust range as needed

        # Start Button
        self.start_button = QPushButton("Start Main Window")

        # Add widgets to layout
        main_layout.addWidget(self.info_label)

        # Allocation Type Section
        allocation_layout = QHBoxLayout()
        allocation_layout.addWidget(self.allocation_label)
        allocation_layout.addWidget(self.allocation_dropdown)
        main_layout.addLayout(allocation_layout)

        # Queue/Partition Section
        queue_layout = QHBoxLayout()
        queue_layout.addWidget(self.queue_label)
        queue_layout.addWidget(self.queue_dropdown)
        main_layout.addLayout(queue_layout)

        # Nodes Section
        nodes_layout = QHBoxLayout()
        nodes_layout.addWidget(self.nodes_label)
        nodes_layout.addWidget(self.nodes_spinbox)
        main_layout.addLayout(nodes_layout)

        # Tasks Section
        tasks_layout = QHBoxLayout()
        tasks_layout.addWidget(self.tasks_label)
        tasks_layout.addWidget(self.tasks_spinbox)
        main_layout.addLayout(tasks_layout)

        # Time Requested Section
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.time_spinbox)
        main_layout.addLayout(time_layout)

        # Start Button
        main_layout.addWidget(self.start_button)

        self.setLayout(main_layout)
        
    def get_inputs(self):
        """Retrieve values from all input fields."""
        return {
            "allocation_type": self.allocation_dropdown.currentText(),
            "queue_partition": self.queue_dropdown.currentText(),
            "num_nodes": self.nodes_spinbox.value(),
            "num_tasks": self.tasks_spinbox.value(),
            "time_requested": self.time_spinbox.value(),
        }

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('gui.ui', self)
        
        # Toggle mode checkbox
        self.toggleModeCheckbox = self.findChild(QCheckBox, 'toggleModeCheckbox')
        self.toggleModeCheckbox.stateChanged.connect(self.toggle_mode)

        # File selection and pseudopotential selection widgets
        self.potentialList = self.findChild(QListWidget, 'potentialList')
        self.finalizeSelectionButton = self.findChild(QPushButton, 'finalizeSelectionButton')
        self.potcarLabel = self.findChild(QLabel, 'potcarLabel')
        self.incarPicker = self.findChild(QPushButton, 'incarPicker')
        self.potcarPicker = self.findChild(QPushButton, 'potcarPicker')
        self.poscarPicker = self.findChild(QPushButton, 'poscarPicker')
        self.runCalcs = self.findChild(QPushButton, 'runCalculations')

        # POSCAR parameter input fields
        self.latticeParameterInput = self.findChild(QLineEdit, 'latticeParameterInput')
        self.atomCountInput = self.findChild(QLineEdit, 'atomCountInput')
        self.atomTypeInput = self.findChild(QLineEdit, 'atomTypeInput')

        # Populate pseudopotential options
        self.potentials = ["PBE_H", "PBE_C", "PBE_O", "LDA_H", "LDA_C", "LDA_O"]  # Replace with actual potentials
        self.potentialList.addItems(self.potentials)

        # Connect buttons to functions
        self.incarPicker.clicked.connect(self.on_clickIncar)
        self.potcarPicker.clicked.connect(self.on_clickPotcar)
        self.poscarPicker.clicked.connect(self.on_clickPoscar)
        self.runCalcs.clicked.connect(self.run_calculations)
        self.finalizeSelectionButton.clicked.connect(self.finalize_selection)

        # Initialize paths and pseudopotentials
        self.incar = ""
        self.poscar = ""
        self.potcar = ""
        self.selected_potentials = []
        self.config = ""

    def toggle_mode(self):
        """Toggle between file selection and manual build mode."""
        manual_mode = self.toggleModeCheckbox.isChecked()
        self.potentialList.setVisible(manual_mode)
        self.finalizeSelectionButton.setVisible(manual_mode)
        self.potcarLabel.setVisible(manual_mode)
        self.incarPicker.setVisible(not manual_mode)
        self.potcarPicker.setVisible(not manual_mode)
        self.poscarPicker.setVisible(not manual_mode)
        self.latticeParameterInput.setVisible(manual_mode)
        self.atomCountInput.setVisible(manual_mode)
        self.atomTypeInput.setVisible(manual_mode)

    def check_all_files_selected(self):
        """Check if all required files have been selected."""
        if self.incar and self.poscar and self.potcar:
            QMessageBox.information(self, "Success", "All required files have been selected!")
        elif self.incar or self.poscar or self.potcar:
            QMessageBox.information(self, "Partial Selection", "Some files have been selected!")

    def on_clickIncar(self):
        incar, _ = QFileDialog.getOpenFileName(self, "Select an INCAR File", "", "All Files (*);;Text Files (*.txt)")
        if incar:
            self.incar = incar
            self.check_all_files_selected()

    def on_clickPoscar(self):
        poscar, _ = QFileDialog.getOpenFileName(self, "Select a POSCAR File", "", "All Files (*);;Text Files (*.txt)")
        if poscar:
            self.poscar = poscar
            self.check_all_files_selected()

    def on_clickPotcar(self):
        potcar, _ = QFileDialog.getOpenFileName(self, "Select a POTCAR File", "", "All Files (*);;Text Files (*.txt)")
        if potcar:
            self.potcar = potcar
            self.check_all_files_selected()

    def finalize_selection(self):
        """Finalize pseudopotential selection."""
        selected_items = self.potentialList.selectedItems()
        self.selected_potentials = [item.text() for item in selected_items]
        if not self.selected_potentials:
            QMessageBox.warning(self, "Error", "Please select at least one pseudopotential!")
            return
        self.build_potcar(self.selected_potentials)

    def build_potcar(self, potential_list):
        """Build POTCAR file from selected potentials."""
        build_potcar(potential_list)
        QMessageBox.information(self, "POTCAR Created", "POTCAR file created successfully!")

    def set_config(self, config):
        self.config = config
    
    def run_calculations(self):
        if not all([self.incar, self.poscar, self.potcar]):
            QMessageBox.warning(self, "Error", "Please select all necessary files before running calculations!")
            return
        calc = Calculations(
            incar=self.incar,
            potcar=self.potcar,
            poscar=self.poscar,
            allocation_type=self.config['allocation_type'],
            queue_partition=self.config['queue_partition'],
            num_nodes=self.config['num_nodes'],
            num_tasks=self.config['num_tasks'],
            time_requested=self.config['time_requested'],
        )
        calc.call_calculations()
        QMessageBox.information(self, "Done", "Calculations completed successfully!")



def main():
    app = QApplication(sys.argv)

    # Splash window setup
    splash = SplashWindow()
    main_window = SimpleApp()

    def start_main_window():
        # Validate inputs on splash window
        config = splash.get_inputs()
        main_window.set_config(config)
        splash.close()
        main_window.show()

    # Connect splash start button to launch main window
    splash.start_button.clicked.connect(start_main_window)

    splash.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
