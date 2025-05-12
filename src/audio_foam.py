import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def estimate_particle_velocity_and_impedance(pressure_values, air_density=1.21, speed_of_sound=343):
    """
    Estimate particle velocity and acoustic impedance from pressure values.

    Args:
        pressure_values: Array of pressure amplitudes (in Pascals).
        air_density: Density of air in kg/m³ (default is 1.21).
        speed_of_sound: Speed of sound in air in m/s (default is 343).

    Returns:
        Tuple of:
            - particle_velocity: Array of particle velocities (in m/s)
            - acoustic_impedance: Array of acoustic impedances (in Rayl)
    """
    Z_air = air_density * speed_of_sound  # Acoustic impedance of air in Rayls

    # Avoid division by zero
    pressure_values = np.asarray(pressure_values)
    particle_velocity = pressure_values / Z_air
    acoustic_impedance = pressure_values / (particle_velocity + 1e-12)  # Numerical stability

    return particle_velocity, acoustic_impedance


def compute_spl(waveform, sample_rate, window_ms=50, p0=20e-6):
    """
    Compute SPL (Sound Pressure Level) over time using RMS in a sliding window.

    Args:
        waveform: Audio waveform (numpy array).
        sample_rate: Sampling rate of the audio (Hz).
        window_ms: Window size for RMS calculation (in milliseconds).
        p0: Reference pressure in Pascals (default is 20 µPa for air).

    Returns:
        Tuple (times, spl_values) for plotting.
    """
    window_size = int(sample_rate * window_ms / 1000)
    num_windows = int(len(waveform) / window_size)
    
    spl_values = []
    times = []

    for i in range(num_windows):
        start = i * window_size
        end = start + window_size
        window = waveform[start:end]

        if len(window) == 0:
            continue

        rms = np.sqrt(np.mean(window**2))
        spl = 20 * np.log10(rms / p0 + 1e-12)  # Add small number to avoid log(0)
        
        spl_values.append(spl)
        times.append(start / sample_rate)

    return np.array(times), np.array(spl_values)

def plot_acoustic_resistivity(p1, v1, p2, v2, sample_rate, window_size):
    """
    Plots acoustic resistivity over time.

    Args:
        pressure_values: Array of pressure values (in Pascals).
        particle_velocity: Array of particle velocity estimates (in m/s).
        sample_rate: Sampling rate of the audio (Hz).
        window_size: Window size used for the original analysis (in samples).

    Returns:
        None (shows plot).
    """
    # Ensure no divide-by-zero
    v1 = np.asarray(v1)
    p1 = np.asarray(p1)
    v2 = np.asarray(v2)
    p2 = np.asarray(p2)
    
    resistivity1 = p1 / (v1 + 1e-12)  # in Rayl
    resistivity2 = p2 / (v2 + 1e-12)  # in Rayl

    # Time array based on windows
    times = np.arange(len(resistivity1)) * (window_size / sample_rate)

    plt.figure(figsize=(12, 5))
    plt.plot(times, resistivity1, label="No Foam")
    plt.plot(times, resistivity2, label="VTP Foam, 2 cm, 500 kPa")
    plt.xlabel("Time (s)")
    plt.ylabel("Acoustic Resistivity (Rayl)")
    plt.title("Acoustic Resistivity Over Time")
    plt.ylim([850, 1250])
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import sys

    # Provide your WAV file pathes here
    wav_path_1 = "../data/0500kPa001SA_foam_sound_absorption_empty_tube.wav"
    wav_path_2 = "../data/0500kPa001SA_foam_sound_absorption_foam.wav"

    sample_rate_1, data_1 = wavfile.read(wav_path_1)
    sample_rate_2, data_2 = wavfile.read(wav_path_2)

    # Convert to mono if stereo
    if data_1.ndim > 1:
        data_1 = data_1.mean(axis=1)

    times_1, spl_1 = compute_spl(data_1.astype(np.float32), sample_rate_1)

    if data_2.ndim > 1:
        data_2 = data_2.mean(axis=1)

    times_2, spl_2 = compute_spl(data_2.astype(np.float32), sample_rate_2)


    # Plotting
    plt.figure(figsize=(12, 5))
    plt.plot(times_1, spl_1, label="No Foam")
    plt.plot(times_2, spl_2, label="500 kPA VTP Foam, 2 cm")
    plt.xlabel("Time (s)")
    plt.ylabel("SPL (dB re 20 µPa)")
    plt.title("Sound Pressure Level Over Time")
    plt.ylim([140,183])
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Rayls test
    
    v1, p1 = estimate_particle_velocity_and_impedance(spl_1)
    v2, p2 = estimate_particle_velocity_and_impedance(spl_2)
    plot_acoustic_resistivity(p1, v1, p2, v2,sample_rate=44100, window_size=2205)