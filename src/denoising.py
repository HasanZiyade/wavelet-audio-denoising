import pywt
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from math import log2
import speechmetrics


def preprocess_signal(signal, noise_std=0.45, random_seed=42):
    """Normalize signal and add noise.
    
    Args:
        signal: Input signal to be processed
        noise_std: Standard deviation of the noise (default: 0.45)
        random_seed: Seed for random noise generation (default: 42)
    """
    # Set random seed
    np.random.seed(random_seed)
    
    # Normalize
    data_reshaped = signal.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(-1, 1))
    normalized_signal = scaler.fit_transform(data_reshaped).flatten()
    
    # Add noise
    noise = np.random.normal(0, noise_std, len(normalized_signal))
    noisy_signal = normalized_signal + noise
    
    # Reset random seed to avoid affecting other random operations
    np.random.seed(None)
    
    return noisy_signal

class WaveletDenoiser:
    def __init__(self, signal, wavelet_type='coif8', level=3, threshold_type='universal', threshold_mode='soft'):
        """Initialize the denoiser with signal and parameters."""
        self.signal = signal
        self.wavelet = wavelet_type
        self.level = level
        self.threshold_type = threshold_type
        self.mode = threshold_mode
        self.coefficients = None
        self.denoised_signal = None

    def decompose(self):
        """Decompose signal using wavelet transform."""
        self.coefficients = pywt.wavedec(self.signal, self.wavelet, level=self.level)

    def threshold(self):
        """Apply thresholding based on selected method."""
        if self.threshold_type == 'SURE':
            self.coefficients = self._SURE()
        elif self.threshold_type == 'HeurSURE':
            self.coefficients = self._HeurSURE()
        elif self.threshold_type == 'minimax':
            self.coefficients = self._Minimax()
        elif self.threshold_type == 'universal':
            self.coefficients = self._universal()
        else:
            raise ValueError("Invalid threshold type")

    def recompose(self):
        """Reconstruct the signal from thresholded coefficients."""
        self.denoised_signal = pywt.waverec(self.coefficients, self.wavelet)
        self.denoised_signal = self.denoised_signal.astype(self.signal.dtype)

    def denoise(self):
        """Main method to perform complete denoising process."""
        self.decompose()
        self.threshold()
        self.recompose()
        return self.denoised_signal

    def _SURE(self):
        """SURE thresholding method."""
        thresholded_coeffs = [self.coefficients[0]]
        for coeff in self.coefficients[1:]:
            m = len(coeff)
            sorted_signal = np.sort(np.abs(coeff))**2
            c = np.linspace(m-1, 0, m)
            s = np.cumsum(sorted_signal)
            risk = [(m - (2.0*(i+1)) + ((m-(i+1)) * sorted_signal[i]) + s[i]) / m for i in range(m)]
            ibest = np.argmin(risk)
            thr = np.sqrt(sorted_signal[ibest])
            thresholded_coeffs.append(pywt.threshold(coeff, value=thr, mode=self.mode))
        return thresholded_coeffs

    def _HeurSURE(self):
        """Heuristic SURE thresholding method."""
        thresholded_coeffs = [self.coefficients[0]]
        for coeff in self.coefficients[1:]:
            m = len(coeff)
            magic = np.sqrt(2 * np.log(m))
            s = [num**2 for num in coeff]
            eta = (np.sum(s) - m) / m
            critical = (log2(m))**(1.5)*np.sqrt(m)
            thr = magic if eta < critical else min(self._SURE(), magic)
            thresholded_coeffs.append(pywt.threshold(coeff, value=thr, mode=self.mode))
        return thresholded_coeffs

    def _Minimax(self):
        """Minimax thresholding method."""
        thresholded_coeffs = [self.coefficients[0]]
        for coeff in self.coefficients[1:]:
            sigma_est = (np.median(np.abs(coeff)))/0.6745
            threshold = sigma_est*(0.3936+0.1829*log2(len(coeff))) if len(coeff) > 32 else 0
            thresholded_coeffs.append(pywt.threshold(coeff, value=threshold, mode=self.mode))
        return thresholded_coeffs

    def _universal(self):
        """Universal thresholding method."""
        thresholded_coeffs = [self.coefficients[0]]
        for coeff in self.coefficients[1:]:
            sigma_est = (np.median(np.abs(coeff)))/0.6745
            threshold = sigma_est*np.sqrt(2*np.log(len(coeff)))
            thresholded_coeffs.append(pywt.threshold(coeff, value=threshold, mode=self.mode))
        return thresholded_coeffs

def compute_metrics(signals_dict, reference_signal, rate, window_length=5):
    """Compute both absolute and relative speech quality metrics."""
    abs_metrics = speechmetrics.load('absolute', window_length)
    rel_metrics = speechmetrics.load(['stoi', 'bsseval', 'sisdr'], window_length)
    results = {}
    
    for signal_name, signal in signals_dict.items():
        # Compute absolute metrics
        abs_scores = abs_metrics(signal, rate=rate)
        # Compute relative metrics using reference signal
        rel_scores = rel_metrics(signal, reference_signal, rate=rate)
        
        results[signal_name] = {
            # Absolute metrics  
            'MOSNET': float(abs_scores['mosnet'][0]),
            'SRMR': float(abs_scores['srmr'][0]),
            # Relative metrics
            'SDR': float(rel_scores['sdr'][0][0]),
            'ISR': float(rel_scores['isr'][0][0]),
            'SAR': float(rel_scores['sar'][0][0]),
            'SISDR': float(rel_scores['sisdr'][0]),
            'STOI': float(rel_scores['stoi'][0])
        }
    
    return results
