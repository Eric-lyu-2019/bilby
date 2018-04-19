import unittest
import peyote.waveform_generator as wg
import numpy as np


def gaussian_frequency_domain_strain(frequency_array, amplitude, mu, sigma, ra, dec, geocent_time, psi):
    ht = {'plus': amplitude * np.exp(-(mu - frequency_array) ** 2 / sigma ** 2 / 2),
          'cross': amplitude * np.exp(-(mu - frequency_array) ** 2 / sigma ** 2 / 2)}
    return ht


class TestWaveformGeneratorInstantiationWithoutOptionalParameters(unittest.TestCase):

    def setUp(self):
        self.waveform_generator = wg.WaveformGenerator(source_model=gaussian_frequency_domain_strain)
        self.simulation_parameters = dict(amplitude=1e-21, mu=100, sigma=1,
                                     ra=1.375,
                                     dec=-1.2108,
                                     geocent_time=1126259642.413,
                                     psi=2.659)

    def tearDown(self):
        del self.waveform_generator
        del self.simulation_parameters

    def test_time_duration(self):
        self.assertEqual(self.waveform_generator.time_duration, 1)

    def test_sampling_frequency(self):
        self.assertEqual(self.waveform_generator.sampling_frequency, 4096)

    def test_source_model(self):
        self.assertEqual(self.waveform_generator.source_model, gaussian_frequency_domain_strain)

    def test_frequency_array_type(self):
        self.assertIsInstance(self.waveform_generator.frequency_array, np.ndarray)

    def test_time_array_type(self):
        self.assertIsInstance(self.waveform_generator.time_array, np.ndarray)

    def test_source_model_parameters(self):
        params = self.simulation_parameters.keys()
        self.assertItemsEqual(self.waveform_generator.parameter_keys, params)


class TestSetValuesFunction(unittest.TestCase):

    def setUp(self):
        self.waveform_generator = wg.WaveformGenerator(source_model=gaussian_frequency_domain_strain)
        self.simulation_parameters = dict(amplitude=1e-21, mu=100, sigma=1,
                                     ra=1.375,
                                     dec=-1.2108,
                                     geocent_time=1126259642.413,
                                     psi=2.659)

    def tearDown(self):
        del self.waveform_generator
        del self.simulation_parameters

    def test_set_values_sets_expected_values_with_expected_keys(self):
        self.waveform_generator.set_values(self.simulation_parameters)
        for key in self.simulation_parameters:
            self.assertEqual(self.waveform_generator.__dict__[key], self.simulation_parameters[key])

    def test_set_values_with_unexpected_keys(self):
        self.simulation_parameters['foo'] = 1337
        self.assertRaises(KeyError, self.waveform_generator.set_values(self.simulation_parameters))