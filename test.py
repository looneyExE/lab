import unittest
from datetime import datetime
from model import WaterMeterReading, ElectricityMeterReading, parse_water_reading, parse_electricity_reading, parse_meter_readings

class TestMeterReadingParsing(unittest.TestCase):

    def test_parse_valid_water_reading(self):
        line = "Вода;01.04.2024;123.45;3.21;456.78"
        reading = parse_water_reading(line)
        reading1 = WaterMeterReading("Вода", datetime(2024, 4, 1), 123.45, 3.21, 456.78)
        self.assertEqual(reading, reading1)

        # self.assertEqual(reading.resource_type, "Вода")
        # self.assertEqual(reading.date, datetime(2024, 4, 1))
        # self.assertAlmostEqual(reading.value, 123.45)
        # self.assertAlmostEqual(reading.flow_rate, 3.21)
        # self.assertAlmostEqual(reading.total_volume, 456.78)

    def test_parse_invalid_water_reading_fields(self):
        line = "Вода;01.04.2024;123.45;3.21"
        with self.assertRaises(ValueError):
            parse_water_reading(line)

    def test_parse_valid_electricity_reading(self):
        line = "Электричество;05.04.2024;321.0;1.23;654.3;50"
        reading = parse_electricity_reading(line)
        self.assertIsInstance(reading, ElectricityMeterReading)
        self.assertEqual(reading.resource_type, "Электричество")
        self.assertEqual(reading.date, datetime(2024, 4, 5))
        self.assertAlmostEqual(reading.value, 321.0)
        self.assertAlmostEqual(reading.power, 1.23)
        self.assertAlmostEqual(reading.total_energy, 654.3)
        self.assertAlmostEqual(reading.frequency, 50.0)

    def test_parse_invalid_electricity_reading_fields(self):
        line = "Электричество;05.04.2024;321.0;1.23;654.3"
        with self.assertRaises(ValueError):
            parse_electricity_reading(line)

    def test_water_str_format(self):
        reading = WaterMeterReading("Вода", datetime(2024, 4, 1), 123.0, 3.0, 456.0)
        self.assertEqual(str(reading), "Вода;01.04.2024;123.0;3.0;456.0")

    def test_electricity_str_format(self):
        reading = ElectricityMeterReading("Электричество", datetime(2024, 4, 5), 321.0, 1.0, 654.0, 50.0)
        self.assertEqual(str(reading), "Электричество;05.04.2024;321.0;1.0;654.0;50.0")

    def test_parse_meter_readings_mixed(self):
        lines = [
            "Вода;01.04.2024;123.45;3.21;456.78",
            "Электричество;05.04.2024;321.0;1.23;654.3;50.0"
        ]
        water_readings, electricity_readings, _ = parse_meter_readings(lines)
        self.assertEqual(len(water_readings + electricity_readings), 2)
        self.assertIsInstance(water_readings[0], WaterMeterReading)
        self.assertIsInstance(electricity_readings[0], ElectricityMeterReading)

    def test_parse_meter_readings_invalid(self):
        lines = [
            "Вода;не-дата;abc;3.21;456.78", 
            "Что-то непонятное",
            "Электричество;05.04.2024;321.0;1.23;654.3"
        ]
        water_readings, electricity_readings, _ = parse_meter_readings(lines)
        self.assertEqual(len(water_readings + electricity_readings), 0)

    def test_parse_meter_readings_partial_valid(self):
        lines = [
            "Вода;01.04.2024;123.45;3.21;456.78",
            "Электричество;invalid;321.0;1.23;654.3;50.0",  
        ]
        water_readings, electricity_readings, _ = parse_meter_readings(lines)
        self.assertEqual(len(water_readings + electricity_readings), 1)
        self.assertIsInstance(water_readings[0], WaterMeterReading)


if __name__ == "__main__":
    unittest.main()
