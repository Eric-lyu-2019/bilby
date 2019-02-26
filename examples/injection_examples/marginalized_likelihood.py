#!/usr/bin/env python
"""
Tutorial to demonstrate how to improve the speed and efficiency of parameter
estimation on an injected signal using time, phase and distance marginalisation.
"""
from __future__ import division, print_function
import bilby
import numpy as np


duration = 4.
sampling_frequency = 2048.
outdir = 'outdir'
label = 'marginalized_likelihood'

np.random.seed(170608)

injection_parameters = dict(
    mass_1=36., mass_2=29., a_1=0.4, a_2=0.3, tilt_1=0.5, tilt_2=1.0,
    phi_12=1.7, phi_jl=0.3, luminosity_distance=4000., theta_jn=0.4, psi=2.659,
    phase=1.3, geocent_time=1126259642.413, ra=1.375, dec=-1.2108)

waveform_arguments = dict(waveform_approximant='IMRPhenomPv2',
                          reference_frequency=50.)

# Create the waveform_generator using a LAL BinaryBlackHole source function
waveform_generator = bilby.gw.WaveformGenerator(
    duration=duration, sampling_frequency=sampling_frequency,
    frequency_domain_source_model=bilby.gw.source.lal_binary_black_hole,
    waveform_arguments=waveform_arguments)

# Set up interferometers.
ifos = bilby.gw.detector.InterferometerList(['H1', 'L1'])
ifos.set_strain_data_from_power_spectral_densities(
    sampling_frequency=sampling_frequency, duration=duration,
    start_time=injection_parameters['geocent_time'] - 3)
ifos.inject_signal(waveform_generator=waveform_generator,
                   parameters=injection_parameters)

# Set up prior
priors = bilby.gw.prior.BBHPriorDict()
# These parameters will not be sampled
for key in ['a_1', 'a_2', 'tilt_1', 'tilt_2', 'phi_12', 'phi_jl', 'theta_jn', 'ra',
            'dec']:
    priors[key] = injection_parameters[key]

# Initialise GravitationalWaveTransient
# Note that we now need to pass the: priors and flags for each thing that's
# being marginalised. A lookup table is used fro distance marginalisation which
# takes a few minutes to build.
likelihood = bilby.gw.GravitationalWaveTransient(
    interferometers=ifos, waveform_generator=waveform_generator, priors=priors,
    distance_marginalization=True, phase_marginalization=True,
    time_marginalization=True)

# Run sampler
result = bilby.run_sampler(
    likelihood=likelihood, priors=priors, sampler='dynesty',
    injection_parameters=injection_parameters, outdir=outdir, label=label)
result.plot_corner()
