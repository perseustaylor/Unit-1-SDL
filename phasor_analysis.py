"""Analyze and plot a single-phase series RLC circuit using phasors."""

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class CircuitResult:
    source_voltage: complex
    impedance: complex
    current: complex
    resistor_voltage: complex
    inductor_voltage: complex
    capacitor_voltage: complex
    inductive_reactance: float
    capacitive_reactance: float
    complex_power: complex


def analyze_series_rlc(
    source_rms: float,
    source_phase_deg: float,
    frequency_hz: float,
    resistance_ohm: float,
    inductance_h: float,
    capacitance_f: float,
) -> CircuitResult:
    """Return steady-state RMS phasors and power for a series RLC circuit."""
    if source_rms < 0:
        raise ValueError("Source RMS voltage cannot be negative.")
    if frequency_hz <= 0:
        raise ValueError("Frequency must be greater than zero.")
    if resistance_ohm < 0 or inductance_h < 0 or capacitance_f < 0:
        raise ValueError("Resistance, inductance, and capacitance cannot be negative.")

    angular_frequency = 2 * np.pi * frequency_hz
    inductive_reactance = angular_frequency * inductance_h
    capacitive_reactance = (
        1 / (angular_frequency * capacitance_f) if capacitance_f > 0 else 0.0
    )

    source_voltage = source_rms * np.exp(1j * np.radians(source_phase_deg))
    impedance = resistance_ohm + 1j * (inductive_reactance - capacitive_reactance)
    if abs(impedance) == 0:
        raise ValueError("Total impedance is zero; current would be undefined.")

    current = source_voltage / impedance
    resistor_voltage = current * resistance_ohm
    inductor_voltage = current * 1j * inductive_reactance
    capacitor_voltage = current * -1j * capacitive_reactance
    complex_power = source_voltage * np.conj(current)

    return CircuitResult(
        source_voltage=source_voltage,
        impedance=impedance,
        current=current,
        resistor_voltage=resistor_voltage,
        inductor_voltage=inductor_voltage,
        capacitor_voltage=capacitor_voltage,
        inductive_reactance=inductive_reactance,
        capacitive_reactance=capacitive_reactance,
        complex_power=complex_power,
    )


def draw_vector(ax: plt.Axes, vector: complex, label: str, color: str) -> None:
    ax.quiver(
        0,
        0,
        vector.real,
        vector.imag,
        angles="xy",
        scale_units="xy",
        scale=1,
        color=color,
        label=label,
        width=0.008,
    )


def plot_results(result: CircuitResult) -> None:
    figure, axes = plt.subplots(2, 2, figsize=(12, 10))
    voltage_ax, current_ax, impedance_ax, power_ax = axes.flat

    voltage_vectors = (
        (result.source_voltage, "Source voltage", "black"),
        (result.resistor_voltage, "Resistor voltage", "tab:blue"),
        (result.inductor_voltage, "Inductor voltage", "tab:red"),
        (result.capacitor_voltage, "Capacitor voltage", "tab:green"),
    )
    for vector, label, color in voltage_vectors:
        if label != "Capacitor voltage" or abs(vector) > 0:
            draw_vector(voltage_ax, vector, label, color)

    configure_vector_axes(
        voltage_ax,
        [vector for vector, _, _ in voltage_vectors],
        "Real voltage (V RMS)",
        "Imaginary voltage (V RMS)",
        "Voltage phasors",
    )
    voltage_ax.legend(loc="best")

    draw_vector(current_ax, result.current, "Current", "tab:orange")
    configure_vector_axes(
        current_ax,
        [result.current],
        "Real current (A RMS)",
        "Imaginary current (A RMS)",
        "Current phasor",
    )
    current_ax.legend(loc="best")

    resistance = result.impedance.real
    net_reactance = result.impedance.imag
    impedance_ax.quiver(
        0, 0, resistance, 0,
        angles="xy", scale_units="xy", scale=1,
        color="tab:blue", label="R",
    )
    impedance_ax.quiver(
        resistance, 0, 0, net_reactance,
        angles="xy", scale_units="xy", scale=1,
        color="tab:red", label="jX (net)",
    )
    impedance_ax.quiver(
        0, 0, result.impedance.real, result.impedance.imag,
        angles="xy", scale_units="xy", scale=1,
        color="black", label="Z",
    )
    configure_vector_axes(
        impedance_ax,
        [result.impedance, complex(resistance, 0)],
        "Resistance (ohm)",
        "Reactance (ohm)",
        "Impedance triangle",
    )
    impedance_ax.legend(loc="best")

    real_power = result.complex_power.real
    reactive_power = result.complex_power.imag
    draw_vector(power_ax, complex(real_power, 0), "P", "tab:blue")
    power_ax.quiver(
        real_power, 0, 0, reactive_power,
        angles="xy", scale_units="xy", scale=1,
        color="tab:red", label="Q",
    )
    draw_vector(power_ax, result.complex_power, "S", "black")
    configure_vector_axes(
        power_ax,
        [result.complex_power, complex(real_power, 0)],
        "Real power, P (W)",
        "Reactive power, Q (var)",
        "Power triangle",
    )
    power_ax.legend(loc="best")

    figure.suptitle("Series RLC Phasor Analysis")
    figure.tight_layout()
    plt.show()


def configure_vector_axes(
    ax: plt.Axes,
    vectors: list[complex],
    x_label: str,
    y_label: str,
    title: str,
) -> None:
    limit = max(max(abs(vector) for vector in vectors) * 1.2, 1.0)
    ax.set(
        xlim=(-limit, limit),
        ylim=(-limit, limit),
        xlabel=x_label,
        ylabel=y_label,
        title=title,
    )
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color="gray", linewidth=0.7)
    ax.axvline(0, color="gray", linewidth=0.7)
    ax.grid(True, alpha=0.3)


def prompt_float(
    label: str,
    default: float,
    minimum: float | None = None,
    minimum_is_exclusive: bool = False,
) -> float:
    while True:
        response = input(f"{label} [{default:g}]: ").strip()
        if not response:
            return default

        try:
            value = float(response)
        except ValueError:
            print("Please enter a number.")
            continue

        if not np.isfinite(value):
            print("Enter a finite number.")
            continue
        if minimum is not None:
            below_minimum = (
                value <= minimum if minimum_is_exclusive else value < minimum
            )
            if below_minimum:
                comparison = "greater than" if minimum_is_exclusive else "at least"
                print(f"Enter a value {comparison} {minimum:g}.")
                continue
        return value


def main() -> None:
    default_frequency = 60.0

    while True:
        print("\nEnter series RLC circuit values. Press Enter to use each default.")
        source_rms = prompt_float("Source voltage (V RMS)", 120.0, 0.0)
        source_phase_deg = prompt_float("Source phase (degrees)", 0.0)
        frequency_hz = prompt_float(
            "Frequency (Hz)", default_frequency, 0.0, minimum_is_exclusive=True
        )
        default_inductance_mh = 15.0 / (2 * np.pi * frequency_hz) * 1000
        resistance_ohm = prompt_float("Resistance (ohm)", 10.0, 0.0)
        inductance_mh = prompt_float(
            "Inductance (mH)", default_inductance_mh, 0.0
        )
        capacitance_uf = prompt_float(
            "Capacitance (uF; enter 0 for none)", 0.0, 0.0
        )

        result = analyze_series_rlc(
            source_rms=source_rms,
            source_phase_deg=source_phase_deg,
            frequency_hz=frequency_hz,
            resistance_ohm=resistance_ohm,
            inductance_h=inductance_mh / 1000,
            capacitance_f=capacitance_uf / 1_000_000,
        )

        impedance_angle_deg = np.angle(result.impedance, deg=True)
        current_angle_deg = np.angle(result.current, deg=True)
        power_factor = abs(np.cos(np.angle(result.impedance)))
        if np.isclose(result.impedance.imag, 0.0, atol=1e-10):
            direction = "unity"
        elif result.impedance.imag > 0:
            direction = "lagging"
        else:
            direction = "leading"
        apparent_power = abs(result.complex_power)

        print(f"\nFrequency: {frequency_hz:.2f} Hz")
        print(
            f"Reactances: X_L = {result.inductive_reactance:.2f} ohm, "
            f"X_C = {result.capacitive_reactance:.2f} ohm"
        )
        print(
            f"Impedance: {abs(result.impedance):.2f} ohm "
            f"at {impedance_angle_deg:.2f} degrees"
        )
        print(
            f"Current: {abs(result.current):.2f} A RMS "
            f"at {current_angle_deg:.2f} degrees"
        )
        print(f"Power factor: {power_factor:.3f} {direction}")
        print(
            f"Power: P = {result.complex_power.real:.2f} W, "
            f"Q = {result.complex_power.imag:.2f} var, "
            f"|S| = {apparent_power:.2f} VA"
        )

        plot_results(result)
        again = input("Analyze another circuit? [y/N]: ").strip().lower()
        if again not in {"y", "yes"}:
            break


if __name__ == "__main__":
    main()