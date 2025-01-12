
# Audio Denoising Application

A Python application for wavelet-based audio denoising through an interactive graphical user interface. This tool enables users to load audio files, apply various denoising algorithms, and evaluate the results using multiple speech quality metrics.

---

## Features

- **Interactive GUI**: User-friendly interface for loading and processing audio files with real-time signal visualization.
- **Multiple Wavelet Types Support**:
  - Daubechies (db1-db38)
  - Symlets (sym2-sym20)
  - Coiflets (coif1-coif17)
  - Biorthogonal (bior1.1-bior6.8)
  - Haar
- **Adjustable Parameters**:
  - Decomposition levels (1-5)
  - Threshold methods:
    - Universal
    - SURE (Stein's Unbiased Risk Estimate)
    - HeurSURE (Heuristic SURE)
    - Minimax
- **Real-time Visualization**: Display of original, noisy, and denoised signals.
- **Audio Playback**: Listen to original, noisy, and denoised audio.
- **Comprehensive Quality Metrics**:
  - MOSNet: Mean Opinion Score (0-5)
  - SRMR: Speech-to-Reverberation Ratio (0-1)
  - SDR: Signal-to-Distortion Ratio (dB)
  - ISR: Image-to-Spatial Ratio (dB)
  - SAR: Signal-to-Artifacts Ratio (dB)
  - SISDR: Scale-Invariant SDR (dB)
  - STOI: Short-Time Objective Intelligibility (0-1)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HasanZiyade/wavelet-audio-denoising
   cd wavelet-audio-denoising
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install `speechmetrics` separately:
   ```bash
   pip install git+https://github.com/aliutkus/speechmetrics#egg=speechmetrics
   ```

### Additional Requirements

If you encounter issues with `speechmetrics` installation on Windows:

1. Download Microsoft Visual C++ Build Tools from:
   [Microsoft Visual C++ Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)
2. Follow installation instructions carefully:
   [Stack Overflow Guide](https://stackoverflow.com/questions/40504552/how-to-install-visual-c-build-tools)

---

## Usage

Run the application:

1. Using the GUI:
   - Click **"Browse"** to select a WAV file.
   - Configure denoising parameters:
     - Wavelet type
     - Decomposition level
     - Threshold method
   - Click **"Process"** to denoise the audio.
   - Use playback controls to compare audio quality.
   - View quality metrics in the metrics panel.

---

## Project Structure

- `main.py`: GUI implementation and application entry point.
- `denoising.py`: Core denoising algorithms and signal processing.
- `requirements.txt`: Required Python packages.

---

## Dependencies

- NumPy: Numerical computing
- SciPy: Scientific computing
- Matplotlib: Plotting
- PyWavelets: Wavelet transforms
- Sounddevice: Audio playback
- Tkinter: GUI framework
- Speechmetrics: Audio quality metrics
- Scikit-learn: Data preprocessing
- Pandas: Data manipulation

---

## Performance Notes

The application's denoising effectiveness depends on:

- Choice of wavelet type
- Decomposition level
- Threshold method
- Input signal characteristics

**Best Results Recommendations:**

- **Decomposition level**: 2-3
- **Wavelet types**: sym6, db6, coif6
- **Threshold type**: Universal or SURE

---

## Testing

The project includes automated testing capabilities through `automated_test.py`, which can:

- Test different wavelet types
- Compare threshold methods
- Analyze decomposition levels
- Generate comprehensive metrics reports

Results of performance analysis are stored in the `results` directory:

- Wavelet comparison metrics
- Threshold method analysis
- Decomposition level impact
- Combined performance metrics

---

## License

This project is open-source and available under the MIT License.

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or new features.
