# AC Phasor Analysis

A small electrical-engineering project for exploring voltage, current, and impedance vectors in a single-phase series RLC circuit.

## Run

Install the dependencies and start the program:

```powershell
python -m pip install -r requirements.txt
python phasor_analysis.py
```

When you start the program, enter the source voltage and phase, frequency, resistance, inductance, and capacitance. Press Enter at a prompt to use its default; enter `0` capacitance for an RL circuit. Inductance is entered in millihenries (mH), and capacitance in microfarads (uF). After each plot closes, choose whether to analyze another circuit. The defaults reproduce the original 120 V RMS source and 10 ohm + j15 ohm load at 60 Hz.

## What it calculates

- Inductive and capacitive reactance from frequency and component values
- Total complex impedance and RMS current phasor
- Resistor, inductor, and capacitor voltage phasors
- Power factor, real power, reactive power, and apparent power
- Separate voltage and current phasor diagrams
- Impedance and power triangles

The source and all reported voltage/current phasors use RMS magnitudes. Complex power is calculated as `S = V * conjugate(I)`, so its real and imaginary parts are real power in watts and reactive power in vars.

## Good next extensions

- Sweep frequency and plot current and power factor against frequency.
- Add parallel RLC circuits and compare series versus parallel resonance.
- Add unit tests for Ohm's law, Kirchhoff's voltage law, and the power triangle.
- Add input controls so component values can be changed without editing the source.