import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import sounddevice as sd
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from denoising import compute_metrics, preprocess_signal, WaveletDenoiser

class AudioDenoisingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Denoising App")
        self.root.geometry("1200x800")  # Increased window size
        
        # Create main frames
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.pack(side="left", fill="y", padx=5, pady=5)
        
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Variables
        self.original_signal = None
        self.noisy_signal = None
        self.denoised_signal = None
        self.sample_rate = None
        self.filename = tk.StringVar()
        
        # Create GUI elements
        self.create_widgets()
        self.create_plot()
        
    def create_plot(self):
        """Create matplotlib plot area."""
        self.fig = Figure(figsize=(6, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def create_widgets(self):
        # File selection
        file_frame = ttk.LabelFrame(self.left_frame, text="File Selection", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(file_frame, textvariable=self.filename).pack(side="left", padx=5)
        ttk.Button(file_frame, text="Browse", command=self.load_file).pack(side="right")
        
        # Parameters frame
        param_frame = ttk.LabelFrame(self.left_frame, text="Denoising Parameters", padding=10)
        param_frame.pack(fill="x", padx=10, pady=5)
        
        # Wavelet type selection
        ttk.Label(param_frame, text="Wavelet Type:").grid(row=0, column=0, padx=5, pady=5)
        self.wavelet_var = tk.StringVar(value="sym4")
        wavelet_combo = ttk.Combobox(param_frame, textvariable=self.wavelet_var)
        wavelet_combo['values'] = ('bior1.1', 'bior1.3', 'bior1.5', 'bior2.2', 'bior2.4', 'bior2.6', 'bior2.8', 'bior3.1', 'bior3.3', 'bior3.5', 'bior3.7', 'bior3.9', 'bior4.4', 'bior5.5', 'bior6.8', 'coif1', 'coif2', 'coif3', 'coif4', 'coif5', 'coif6', 'coif7', 'coif8', 'coif9', 'coif10', 'coif11', 'coif12', 'coif13', 'coif14', 'coif15', 'coif16', 'coif17', 'db1', 'db2', 'db3', 'db4', 'db5', 'db6', 'db7', 'db8', 'db9', 'db10', 'db11', 'db12', 'db13', 'db14', 'db15', 'db16', 'db17', 'db18', 'db19', 'db20', 'db21', 'db22', 'db23', 'db24', 'db25', 'db26', 'db27', 'db28', 'db29', 'db30', 'db31', 'db32', 'db33', 'db34', 'db35', 'db36', 'db37', 'db38', 'dmey', 'haar', 'rbio1.1', 'rbio1.3', 'rbio1.5', 'rbio2.2', 'rbio2.4', 'rbio2.6', 'rbio2.8', 'rbio3.1', 'rbio3.3', 'rbio3.5', 'rbio3.7', 'rbio3.9', 'rbio4.4', 'rbio5.5', 'rbio6.8', 'sym2', 'sym3', 'sym4', 'sym5', 'sym6', 'sym7', 'sym8', 'sym9', 'sym10', 'sym11', 'sym12', 'sym13', 'sym14', 'sym15', 'sym16', 'sym17', 'sym18', 'sym19', 'sym20')
        wavelet_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Level selection
        ttk.Label(param_frame, text="Decomposition Level:").grid(row=1, column=0, padx=5, pady=5)
        self.level_var = tk.IntVar(value=3)
        level_combo = ttk.Combobox(param_frame, textvariable=self.level_var)
        level_combo['values'] = (1, 2, 3, 4, 5)
        level_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Threshold type selection
        ttk.Label(param_frame, text="Threshold Type:").grid(row=2, column=0, padx=5, pady=5)
        self.threshold_var = tk.StringVar(value="universal")
        threshold_combo = ttk.Combobox(param_frame, textvariable=self.threshold_var)
        threshold_combo['values'] = ('universal', 'SURE', 'HeurSURE', 'minimax')
        threshold_combo.grid(row=2, column=1, padx=5, pady=5)
        
        # Process button
        ttk.Button(param_frame, text="Process", command=self.process_audio).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Playback frame
        play_frame = ttk.LabelFrame(self.left_frame, text="Playback Controls", padding=10)
        play_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(play_frame, text="Play Original", command=lambda: self.play_audio('original')).pack(side="left", padx=5)
        ttk.Button(play_frame, text="Play Noisy", command=lambda: self.play_audio('noisy')).pack(side="left", padx=5)
        ttk.Button(play_frame, text="Play Denoised", command=lambda: self.play_audio('denoised')).pack(side="left", padx=5)
        
        # Metrics display
        self.metrics_frame = ttk.LabelFrame(self.left_frame, text="Quality Metrics", padding=10)
        self.metrics_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.metrics_text = tk.Text(self.metrics_frame, height=10)
        self.metrics_text.pack(fill="both", expand=True)
        
    def update_plot(self):
        """Update the matplotlib plot with current signals."""
        self.fig.clear()
        
        # Create three subplots
        ax1 = self.fig.add_subplot(311)
        ax2 = self.fig.add_subplot(312)
        ax3 = self.fig.add_subplot(313)
        
        # Plot signals
        if self.original_signal is not None:
            ax1.plot(self.original_signal)
            ax1.set_title('Original Signal')
            ax1.set_xticks([])
            
        if self.noisy_signal is not None:
            ax2.plot(self.noisy_signal)
            ax2.set_title('Noisy Signal')
            ax2.set_xticks([])
            
        if self.denoised_signal is not None:
            ax3.plot(self.denoised_signal)
            ax3.set_title('Denoised Signal')
            
        self.fig.tight_layout()
        self.canvas.draw()
    
    def process_audio(self):
        if self.original_signal is None:
            messagebox.showerror("Error", "Please load an audio file first")
            return
            
        # Preprocess
        self.noisy_signal = preprocess_signal(self.original_signal)
        
        # Create denoiser and process
        denoiser = WaveletDenoiser(
            self.noisy_signal,
            wavelet_type=self.wavelet_var.get(),
            level=self.level_var.get(),
            threshold_type=self.threshold_var.get()
        )
        self.denoised_signal = denoiser.denoise()
        
        # Update plot
        self.update_plot()
        
        # Compute metrics for noisy and denoised signals
        signals = {
            'Noisy': self.noisy_signal,
            'Denoised': self.denoised_signal
        }
        
        scores = compute_metrics(signals, self.original_signal, self.sample_rate)
        
        # Display metrics in an organized way
        self.metrics_text.delete(1.0, tk.END)
        
        # Display denoising parameters
        self.metrics_text.insert(tk.END, "Denoising Parameters:\n")
        self.metrics_text.insert(tk.END, f"Wavelet Type: {self.wavelet_var.get()}\n")
        self.metrics_text.insert(tk.END, f"Decomposition Level: {self.level_var.get()}\n")
        self.metrics_text.insert(tk.END, f"Threshold Type: {self.threshold_var.get()}\n\n")
        
        self.metrics_text.insert(tk.END, "Speech Quality Metrics:\n\n")
        
        # Metric descriptions
        self.metrics_text.insert(tk.END, "Metrics Description:\n")
        self.metrics_text.insert(tk.END, "- MOSNet (0-5): Mean Opinion Score, higher is better\n")
        self.metrics_text.insert(tk.END, "- SRMR (0-1): Speech-to-Reverberation Modulation Ratio, higher is better\n")
        self.metrics_text.insert(tk.END, "- SDR (dB): Signal-to-Distortion Ratio, higher is better\n")
        self.metrics_text.insert(tk.END, "- ISR (dB): Image-to-Spatial Ratio, higher is better\n")
        self.metrics_text.insert(tk.END, "- SAR (dB): Signal-to-Artifacts Ratio, higher is better\n")
        self.metrics_text.insert(tk.END, "- SISDR (dB): Scale-Invariant Signal-to-Distortion Ratio, higher is better\n")
        self.metrics_text.insert(tk.END, "- STOI (0-1): Short-Time Objective Intelligibility, higher is better\n\n")
        
        # Absolute Metrics Section
        self.metrics_text.insert(tk.END, "Absolute Metrics:\n")
        header_abs = f"{'Signal Type':<15} {'MOSNet':<10} {'SRMR':<10}\n"
        separator = "-" * 35 + "\n"
        
        self.metrics_text.insert(tk.END, header_abs)
        self.metrics_text.insert(tk.END, separator)
        
        for signal_type, metrics in scores.items():
            line = f"{signal_type:<15} {metrics['MOSNET']:<10.3f} {metrics['SRMR']:<10.3f}\n"
            self.metrics_text.insert(tk.END, line)
            
        # Relative Metrics Section
        self.metrics_text.insert(tk.END, "\nRelative Metrics:\n")
        header_rel = f"{'Signal Type':<15} {'SDR':<8} {'ISR':<8} {'SAR':<8} {'SISDR':<8} {'STOI':<8}\n"
        separator = "-" * 55 + "\n"
        
        self.metrics_text.insert(tk.END, header_rel)
        self.metrics_text.insert(tk.END, separator)
        
        for signal_type, metrics in scores.items():
            line = f"{signal_type:<15} {metrics['SDR']:<8.2f} {metrics['ISR']:<8.2f} {metrics['SAR']:<8.2f} "
            line += f"{metrics['SISDR']:<8.2f} {metrics['STOI']:<8.2f}\n"
            self.metrics_text.insert(tk.END, line)

    def load_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("WAV files", "*.wav")]
        )
        if filepath:
            self.filename.set(filepath)
            self.sample_rate, self.original_signal = wav.read(filepath)
            self.original_signal = (self.original_signal - np.min(self.original_signal)) / (np.max(self.original_signal) - np.min(self.original_signal))
            # Update plot with original signal
            self.update_plot()
        
    def play_audio(self, audio_type):
        if audio_type == 'original' and self.original_signal is not None:
            sd.play(self.original_signal, self.sample_rate)
        elif audio_type == 'noisy' and self.noisy_signal is not None:
            sd.play(self.noisy_signal, self.sample_rate)
        elif audio_type == 'denoised' and self.denoised_signal is not None:
            sd.play(self.denoised_signal, self.sample_rate)
        else:
            messagebox.showerror("Error", "Audio not available")
        sd.wait()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioDenoisingGUI(root)
    root.mainloop()