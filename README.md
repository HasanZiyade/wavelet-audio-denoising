
# Audio Denoising Application

A Python application for wavelet-based audio denoising through an interactive graphical user interface. This tool enables users to load audio files, apply various denoising algorithms, and evaluate the results using multiple speech quality metrics. The denoising will be made using Python and mainly utilizing the ‘pywt’ library which is a free Open Source library for wavelet transforms in Python.

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

## Main Algorithm
The main algorithm follows simple steps of signal denoising: 
### Preprocessing
- The audio file is turned it into a numpy array.
- Signal is normalized between -1 and 1.
- Simulated white gaussian noise added to the signal.
### Decomposition
- The decomposition will be made based on selected wavelet type and decomposition level.
- Detail and approximation coefficients are returned for each level.
### Thresholding
- Soft thresholding is applied to all signals 
- The detail coefficients will be thresholded using the selected method.
### Recomposition
- The signal will be recomposed using pywt functions
- Parameters for the recomposition are the same as the decomposition function 

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

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any improvements or new features.
