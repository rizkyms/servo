import os
import cv2
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print(f"ERROR: creating directory with name {path}")

def save_frame(video_path, save_dir, gap=5, prefix="frame", progress_callback=None, stop_event=None):
    name = os.path.basename(video_path).split(".")[0]
    save_path = os.path.join(save_dir, name)
    create_dir(save_path)

    cap = cv2.VideoCapture(video_path)
    idx = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total_extractable_frames = total_frames // gap
    extracted_frames = 0

    while not stop_event.is_set():
        ret, frame = cap.read()

        if not ret:
            cap.release()
            break

        if idx % gap == 0:
            cv2.imwrite(os.path.join(save_path, f"{prefix}_{idx}.png"), frame)
            extracted_frames += 1

            if progress_callback:
                progress_callback(extracted_frames / total_extractable_frames * 100)

        idx += 1

    cap.release()
    if not stop_event.is_set() and progress_callback:
        progress_callback(100, finished=True)

class FrameExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Frame Converter")
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_label = ttk.Label(self.main_frame, text="Input Video File:")
        self.input_label.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.input_entry = ttk.Entry(self.main_frame, width=40)
        self.input_entry.grid(row=0, column=1, pady=5)

        self.input_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_input_file)
        self.input_button.grid(row=0, column=2, padx=5, pady=5)

        self.output_label = ttk.Label(self.main_frame, text="Output Directory:")
        self.output_label.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.output_entry = ttk.Entry(self.main_frame, width=40)
        self.output_entry.grid(row=1, column=1, pady=5)

        self.output_button = ttk.Button(self.main_frame, text="Browse", command=self.browse_output_dir)
        self.output_button.grid(row=1, column=2, padx=5, pady=5)

        self.prefix_label = ttk.Label(self.main_frame, text="File Prefix:")
        self.prefix_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.prefix_entry = ttk.Entry(self.main_frame, width=10)
        self.prefix_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.gap_label = ttk.Label(self.main_frame, text="Frame Gap:")
        self.gap_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        self.gap_entry = ttk.Entry(self.main_frame, width=10)
        self.gap_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        self.run_button = ttk.Button(self.main_frame, text="Run", command=self.run_extraction)
        self.run_button.grid(row=4, column=0, pady=10)

        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop_extraction)
        self.stop_button.grid(row=4, column=1, pady=10)

        self.progress = ttk.Progressbar(self.main_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)

    def browse_input_file(self):
        input_file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if input_file:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, input_file)

    def browse_output_dir(self):
        output_dir = filedialog.askdirectory()
        if output_dir:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_dir)

    def update_progress(self, value, finished=False):
        self.progress['value'] = value
        self.root.update_idletasks()
        if finished:
            messagebox.showinfo("Completed", "Frame extraction completed successfully")

    def run_extraction(self):
        self.stop_event.clear()
        input_file = self.input_entry.get()
        output_dir = self.output_entry.get()
        prefix = self.prefix_entry.get()
        gap = self.gap_entry.get()

        if not input_file or not output_dir or not gap or not prefix:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            gap = int(gap)
        except ValueError:
            messagebox.showerror("Error", "Gap must be an integer")
            return

        self.progress['value'] = 0
        self.root.update_idletasks()

        self.extraction_thread = threading.Thread(
            target=save_frame,
            args=(input_file, output_dir, gap, prefix, self.update_progress, self.stop_event)
        )
        self.extraction_thread.start()

    def stop_extraction(self):
        self.stop_event.set()
        self.extraction_thread.join()
        messagebox.showinfo("Stopped", "Frame extraction stopped")

def main():
    root = tk.Tk()
    app = FrameExtractorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
