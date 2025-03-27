from datetime import datetime
from typing import List
from PyQt5 import QtWidgets

class MeterReading:
    def __init__(self, resource_type: str, date: datetime, value: float):
        self.resource_type = resource_type
        self.date = date
        self.value = value


'''
1) MeterReading.__new__() -> self
2) MeterReading.__init__(self)

Summary: a = MeterReading.__init__(MeterReading.__new__())
'''

class WaterMeterReading(MeterReading):
    def __init__(self, resource_type: str, date: datetime, value: float, flow_rate: float, total_volume: float):
        super().__init__(resource_type, date, value)
        self.flow_rate = flow_rate
        self.total_volume = total_volume

    def __str__(self):
        return f"{self.resource_type};{self.date.strftime('%d.%m.%Y')};{self.value};{self.flow_rate};{self.total_volume}"

class ElectricityMeterReading(MeterReading):
    def __init__(self, resource_type: str, date: datetime, value: float, power: float, total_energy: float, frequency: float):
        super().__init__(resource_type, date, value)
        self.power = power
        self.total_energy = total_energy
        self.frequency = frequency

    def __str__(self):
        return f"{self.resource_type};{self.date.strftime('%d.%m.%Y')};{self.value};{self.power};{self.total_energy};{self.frequency}"

def parse_water_reading(line: str) -> WaterMeterReading:
    parts = line.strip().split(';')
    return WaterMeterReading(
        resource_type=parts[0],
        date=datetime.strptime(parts[1], '%d.%m.%Y'),
        value=float(parts[2].replace(',', '.')),
        flow_rate=float(parts[3].replace(',', '.')),
        total_volume=float(parts[4].replace(',', '.'))
    )

def parse_electricity_reading(line: str) -> ElectricityMeterReading:
    parts = line.strip().split(';')
    return ElectricityMeterReading(
        resource_type=parts[0],
        date=datetime.strptime(parts[1], '%d.%m.%Y'),
        value=float(parts[2].replace(',', '.')),
        power=float(parts[3].replace(',', '.')),
        total_energy=float(parts[4].replace(',', '.')),
        frequency=float(parts[5].replace(',', '.'))
    )

def read_file(file_path: str) -> List[str]:
    with open(file_path, 'r') as file:
        return file.readlines()

def write_file(file_path: str, water_readings: List[WaterMeterReading], electricity_readings: List[ElectricityMeterReading]):
    with open(file_path, 'w') as file:
        for reading in water_readings:
            file.write(str(reading) + '\n')
        for reading in electricity_readings:
            file.write(str(reading) + '\n')

def parse_meter_readings(lines: List[str]):
    water_readings = []
    electricity_readings = []

    for line in lines:
        if line.startswith('Вода'):
            water_readings.append(parse_water_reading(line))
        elif line.startswith('Электричество'):
            electricity_readings.append(parse_electricity_reading(line))
    
    return water_readings, electricity_readings

class AddReadingDialog(QtWidgets.QDialog):
    def __init__(self, parent=False):
        super().__init__(parent)
        self.setWindowTitle("Добавить новый объект")
        self.setGeometry(200, 200, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Тип ресурса
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.addItems(["Вода", "Электричество"])
        layout.addWidget(QtWidgets.QLabel("Тип ресурса:"))
        layout.addWidget(self.type_combo)
        
        # Дата
        self.date_edit = QtWidgets.QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(datetime.today().date())
        layout.addWidget(QtWidgets.QLabel("Дата:"))
        layout.addWidget(self.date_edit)
        
        # Значения
        self.value_edit = QtWidgets.QLineEdit()
        self.flow_rate_edit = QtWidgets.QLineEdit()
        self.total_volume_edit = QtWidgets.QLineEdit()
        self.frequency_edit = QtWidgets.QLineEdit()
        
        layout.addWidget(QtWidgets.QLabel("Значение:"))
        layout.addWidget(self.value_edit)
        layout.addWidget(QtWidgets.QLabel("Мгновенное значение (flow/power):"))
        layout.addWidget(self.flow_rate_edit)
        layout.addWidget(QtWidgets.QLabel("Общее потребление (volume/energy):"))
        layout.addWidget(self.total_volume_edit)
        layout.addWidget(QtWidgets.QLabel("Частота (frequency, только для электричества):"))
        layout.addWidget(self.frequency_edit)
        
        self.ok_button = QtWidgets.QPushButton("Добавить")
        self.ok_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.ok_button)
        
        self.setLayout(layout)

    def validate_and_accept(self):
        try:
            float(self.value_edit.text())
            if self.type_combo.currentText() == "Вода":
                if self.frequency_edit.text():
                    self.frequency_edit.setStyleSheet("background-color: red;")
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Частота не должна быть введена для воды!")
                    return
                float(self.flow_rate_edit.text())
                float(self.total_volume_edit.text())
            else:
                float(self.flow_rate_edit.text())
                float(self.total_volume_edit.text())
                float(self.frequency_edit.text())
            self.accept()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректные числовые значения.")
    
    def get_data(self):
        if self.type_combo.currentText() == "Вода":
            return {
                'type': self.type_combo.currentText(),
                'date': self.date_edit.date().toString("dd.MM.yyyy"),
                'value': self.value_edit.text(),
                'flow_rate': self.flow_rate_edit.text(),
                'total_volume': self.total_volume_edit.text()
            }
        else:
            return {
                'type': self.type_combo.currentText(),
                'date': self.date_edit.date().toString("dd.MM.yyyy"),
                'value': self.value_edit.text(),
                'power': self.flow_rate_edit.text(),
                'total_energy': self.total_volume_edit.text(),
                'frequency': self.frequency_edit.text()
            }


class MeterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Meter Readings")
        self.setGeometry(100, 100, 800, 600)
        
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(10, 10, 780, 500)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Тип", "Дата", "Значение", "Мгновенное значение", "Общее потребление", "Частота"])
        
        self.load_button = QtWidgets.QPushButton("Загрузить", self)
        self.load_button.setGeometry(10, 520, 100, 30)
        self.load_button.clicked.connect(self.select_file_to_load)
        
        self.add_button = QtWidgets.QPushButton("Добавить", self)
        self.add_button.setGeometry(120, 520, 100, 30)
        self.add_button.clicked.connect(self.add_item)
        
        self.delete_button = QtWidgets.QPushButton("Удалить", self)
        self.delete_button.setGeometry(230, 520, 100, 30)
        self.delete_button.clicked.connect(self.delete_item)
        
        self.save_button = QtWidgets.QPushButton("Сохранить", self)
        self.save_button.setGeometry(340, 520, 100, 30)
        self.save_button.clicked.connect(self.select_file_to_save)
        
        self.water_readings = []
        self.electricity_readings = []
        self.file_path = ""

    def select_file_to_load(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл для загрузки", "", "CSV Files (*.csv)")
        if file_name:
            self.file_path = file_name
            self.load_data()
    
    def select_file_to_save(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Выбрать файл для сохранения", "", "CSV Files (*.csv)")
        if file_name:
            self.file_path = file_name
            self.save_data()
    
    def load_data(self):
        if not self.file_path:
            return
        lines = read_file(self.file_path)
        self.water_readings, self.electricity_readings = parse_meter_readings(lines)
        
        self.table.setRowCount(0)
        for reading in self.water_readings + self.electricity_readings:
            row = self.table.rowCount()
            self.table.insertRow(row)
            data = str(reading).split(';')
            for col, item in enumerate(data):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(item))
    
    def add_item(self):
        dialog = AddReadingDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            row = self.table.rowCount()
            self.table.insertRow(row)
            for col, value in enumerate(data.values()):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
    
    def delete_item(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)
    
    def save_data(self):
        self.water_readings = []
        self.electricity_readings = []
        for row in range(self.table.rowCount()):
            data = [self.table.item(row, col).text() if self.table.item(row, col) else "" for col in range(6)]
            if data[0] == "Вода":
                self.water_readings.append(parse_water_reading(';'.join(data)))
            elif data[0] == "Электричество":
                self.electricity_readings.append(parse_electricity_reading(';'.join(data)))
        write_file(self.file_path, self.water_readings, self.electricity_readings)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MeterApp()
    window.show()
    sys.exit(app.exec_())
