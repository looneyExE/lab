from datetime import datetime
from typing import List

class MeterReading:
    def __init__(self, resource_type: str, date: datetime, value: float):
        self.resource_type = resource_type
        self.date = date
        self.value = value

class WaterMeterReading(MeterReading):
    def __init__(self, resource_type: str, date: datetime, value: float, flow_rate: float, total_volume: float):
        super().__init__(resource_type, date, value)
        self.flow_rate = flow_rate
        self.total_volume = total_volume

    def __str__(self):
        return f"{self.resource_type};{self.date.strftime('%d.%m.%Y')};{self.value};{self.flow_rate};{self.total_volume}"
    
    def __eq__(self, other):
        if isinstance(other, WaterMeterReading):
            return (self.resource_type == other.resource_type and
                         self.date == other.date and
                         self.value == other.value and
                         self.flow_rate == other.flow_rate and
                         self.total_volume == other.total_volume)
        return NotImplemented

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
    if len(parts) != 5:
        raise ValueError("Неверное количество полей для водяного счётчика.")
    return WaterMeterReading(
        resource_type=parts[0],
        date=datetime.strptime(parts[1], '%d.%m.%Y'),
        value=float(parts[2].replace(',', '.')),
        flow_rate=float(parts[3].replace(',', '.')),
        total_volume=float(parts[4].replace(',', '.'))
    )

def parse_electricity_reading(line: str) -> ElectricityMeterReading:
    parts = line.strip().split(';')
    if len(parts) != 6:
        raise ValueError("Неверное количество полей для электрического счётчика.")
    return ElectricityMeterReading(
        resource_type=parts[0],
        date=datetime.strptime(parts[1], '%d.%m.%Y'),
        value=float(parts[2].replace(',', '.')),
        power=float(parts[3].replace(',', '.')),
        total_energy=float(parts[4].replace(',', '.')),
        frequency=float(parts[5].replace(',', '.'))
    )

def read_file(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(file_path: str, water_readings: List[WaterMeterReading], electricity_readings: List[ElectricityMeterReading]):
    with open(file_path, 'w', encoding='utf-8') as file:
        for reading in water_readings:
            file.write(str(reading) + '\n')
        for reading in electricity_readings:
            file.write(str(reading) + '\n')

def parse_meter_readings(lines: List[str]):
    water_readings = []
    electricity_readings = []
    errors = []
    for idx, line in enumerate(lines):
        try:
            if line.startswith('Вода'):
                water_readings.append(parse_water_reading(line))
            elif line.startswith('Электричество'):
                electricity_readings.append(parse_electricity_reading(line))
        except Exception as e:
            errors.append(f"Ошибка в строке {idx + 1}: {e}")

    return water_readings, electricity_readings, errors
