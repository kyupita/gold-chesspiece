import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk
import os
import glob
import sys

# --- Global Variables and Constants ---
new_pivots = {}    # Stores the new pivots for the current image
CHESSP_DIR = "exported"    # Main directory for the chess pieces
IMAGES_FOLDER_NAME = "swap_body"    # Fixed name for the images folder
MAX_WINDOW_WIDTH = 700    # Maximum window width
MAX_CANVAS_SIZE = 480    # Maximum size for the canvas inside the window

# --- Utility Functions ---

def get_target_image_data(root):
    """Extracts IDs, names, and pivots for 'swap_body-X.png' images."""
    data = []
    folder_element = root.find("./folder")
    
    if folder_element is not None:
        for file_element in folder_element.findall("./file"):
            file_name = file_element.get('name', '')
            
            # Filter only images containing "swap_body-"
            if "swap_body-" in file_name:
                file_id = file_element.get('id')
                pivot_x = file_element.get('pivot_x')
                pivot_y = file_element.get('pivot_y')
                
                if file_id and pivot_x and pivot_y:
                    data.append((file_id, file_name, pivot_x, pivot_y))
    
    return data

# --- Execution Mode Detection Logic ---

def get_execution_mode():
    """
    Determines if the script is running:
    1. Inside a 'chesspiece_algo' folder (Single Mode)
    2. Inside the parent folder of 'exported/' (Batch Mode)
    """
    current_dir = os.getcwd()
    
    # Mode 1: Inside a chesspiece_algo folder
    if os.path.basename(current_dir).startswith("chesspiece_"):
        scml_files = [f for f in os.listdir(current_dir) if f.startswith("swap_") and f.endswith(".scml")]
        images_path = os.path.join(current_dir, IMAGES_FOLDER_NAME)
        
        if scml_files and os.path.isdir(images_path):
            return "SINGLE", [(os.path.join(current_dir, scml_files[0]), images_path)]
    
    # Mode 2: Inside the parent directory of 'exported'
    exported_path = os.path.join(current_dir, CHESSP_DIR)
    if os.path.isdir(exported_path):
        chesspiece_dirs = glob.glob(os.path.join(exported_path, "chesspiece_*"))
        
        if chesspiece_dirs:
            file_list = []
            for cp_dir in chesspiece_dirs:
                scml_files = [f for f in os.listdir(cp_dir) if f.startswith("swap_") and f.endswith(".scml")]
                images_path = os.path.join(cp_dir, IMAGES_FOLDER_NAME)
                
                if scml_files and os.path.isdir(images_path):
                    file_list.append((os.path.join(cp_dir, scml_files[0]), images_path))
            
            if file_list:
                return "BATCH", file_list

    return "NONE", []

# --- Main Flow Controller (BATCH Mode) ---

class ChessPieceManager:
    def __init__(self, master, file_list):
        self.master = master
        self.file_list = file_list    # List of tuples (scml_path, images_path)
        self.current_chesspiece_index = 0
        self.editor_app = None
        
        self.start_next_chesspiece()

    def get_chesspiece_name(self):
        """Returns the folder name (chesspiece_...)."""
        if self.current_chesspiece_index < len(self.file_list):
            scml_path, _ = self.file_list[self.current_chesspiece_index]
            return os.path.basename(os.path.dirname(scml_path))
        return "N/A"
        
    def start_next_chesspiece(self):
        """Starts the editor for the next piece or finishes."""
        if self.editor_app and self.editor_app.master:
            self.editor_app.master.destroy() # Closes the previous editor window

        if self.current_chesspiece_index >= len(self.file_list):
            messagebox.showinfo("Process Complete", "All chesspieces have been processed. Done!")
            
            # --- KEY CORRECTION ---
            # Call quit() on the hidden main window (root)
            self.master.quit() 
            # ------------------------
            
            return
            
        scml_path, images_folder = self.file_list[self.current_chesspiece_index]
            
        try:
            tree = ET.parse(scml_path)
            root = tree.getroot()
            target_images = get_target_image_data(root)
            
            if not target_images:
                messagebox.showinfo("Info", f"No images found in {self.get_chesspiece_name()}. Skipping...")
                self.current_chesspiece_index += 1
                self.start_next_chesspiece()
                return

            # Create a new window for the editor (Toplevel)
            editor_window = tk.Toplevel(self.master)
            self.editor_app = PivotEditorApp(editor_window, scml_path, images_folder, target_images, self)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error processing '{self.get_chesspiece_name()}': {e}")
            self.current_chesspiece_index += 1
            self.start_next_chesspiece()
            
    def move_to_next(self):
        """Advances the index and calls start_next_chesspiece."""
        # Ensure the current editor is destroyed ONLY HERE before advancing.
        if self.editor_app and self.editor_app.master:
            self.editor_app.master.destroy()
            
        self.current_chesspiece_index += 1
        self.start_next_chesspiece()

# --- User Interface and Logic Functions ---

class PivotEditorApp:
    def __init__(self, master, file_path, images_dir, image_data, manager=None):
        self.master = master
        self.manager = manager # None in SINGLE mode, ChessPieceManager in BATCH mode
        master.title(f"Pivot Editor - {manager.get_chesspiece_name() if manager else os.path.basename(os.path.dirname(file_path))}")
        
        # Load XML
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()
        self.file_path = file_path
        self.images_dir = images_dir
        
        # Image data to edit
        self.image_data = image_data
        self.current_image_index = 0
        self.total_images = len(image_data)
        
        self.pivot_center = (0, 0)
        global new_pivots
        new_pivots = {} # Clear for each new piece or execution
        
        # ----------------------------------------------------
        # Window and Scrollbar Configuration
        # ----------------------------------------------------
        
        # 1. Limit window width
        master.maxsize(width=MAX_WINDOW_WIDTH, height=900)
        master.minsize(width=MAX_WINDOW_WIDTH, height=700)

        # 2. Main frame with Scrollbar
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas_scroll = tk.Canvas(self.main_frame, width=MAX_WINDOW_WIDTH-20)
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas_scroll.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas_scroll, width=MAX_WINDOW_WIDTH)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas_scroll.configure(
                scrollregion=self.canvas_scroll.bbox("all")
            )
        )

        self.canvas_scroll.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas_scroll.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas_scroll.pack(side="left", fill="both", expand=True)

        if self.manager:
            master.protocol("WM_DELETE_WINDOW", self.close_editor)
        
        # ----------------------------------------------------
        # Application Content inside scrollable_frame
        # ----------------------------------------------------

        # 0. Current piece label
        chesspiece_name = manager.get_chesspiece_name() if manager else os.path.basename(os.path.dirname(file_path))
        self.chesspiece_label = ttk.Label(self.scrollable_frame, text=f"Editing: {chesspiece_name}", font=('Arial', 12, 'bold'))
        self.chesspiece_label.pack(pady=10)

        # 1. Canvas Configuration (Image visualization area)
        self.canvas_frame = ttk.Frame(self.scrollable_frame)
        self.canvas_frame.pack(padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=MAX_CANVAS_SIZE, height=MAX_CANVAS_SIZE, bg='gray')
        self.canvas.pack(side=tk.LEFT)
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        
        # 2. Controls Configuration
        self.controls_frame = ttk.Frame(self.scrollable_frame)
        self.controls_frame.pack(padx=10, pady=10)
        
        self.image_label = ttk.Label(self.controls_frame, text="")
        self.image_label.pack()
        
        self.pivot_info_label = ttk.Label(self.controls_frame, text="Pivot: X: 0.00, Y: 0.00")
        self.pivot_info_label.pack(pady=5)
        
        button_frame = ttk.Frame(self.controls_frame)
        button_frame.pack(pady=10)
        
        self.next_button = ttk.Button(button_frame, text="Next Image", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        finish_text = "Done / Next ChessPiece" if manager else "Done and Save"
        self.finish_button = ttk.Button(button_frame, text=finish_text, command=self.finish_editing)
        self.finish_button.pack(side=tk.LEFT, padx=5)
        self.finish_button["state"] = "disabled"
        
        # Start with the first image
        self.load_image()
        
        # Adjust scroll upon initial content load
        master.update_idletasks()
        self.canvas_scroll.config(scrollregion=self.canvas_scroll.bbox("all"))

    def close_editor(self):
        """Closes the current editor window and stops the program if necessary (e.g., closing with the 'X')."""
        
        # 1. Destroy the current window (Toplevel or root)
        self.master.destroy() 
        
        # 2. If in BATCH mode and manager exists, stop the mainloop.
        if self.manager:
            self.manager.master.quit() # Stops the root.mainloop()

    def load_image(self):
        """Loads the current image and positions the initial pivot (Y inverted)."""
        if self.current_image_index >= self.total_images:
            return

        file_id, file_name, pivot_x_str, pivot_y_str = self.image_data[self.current_image_index]
        image_path = os.path.join(self.images_dir, os.path.basename(file_name))
        
        self.image_label.config(text=f"Image {self.current_image_index + 1}/{self.total_images}: {os.path.basename(file_name)}")
        
        try:
            img = Image.open(image_path)
            image_original_size = img.size
            canvas_w, canvas_h = MAX_CANVAS_SIZE, MAX_CANVAS_SIZE

            # 1. Scale calculation
            scale_w = canvas_w / image_original_size[0]
            scale_h = canvas_h / image_original_size[1]
            self.scale_factor = min(scale_w, scale_h, 1.0)
            
            new_w = max(1, int(image_original_size[0] * self.scale_factor))
            new_h = max(1, int(image_original_size[1] * self.scale_factor))
            
            self.image_tk = ImageTk.PhotoImage(img.resize((new_w, new_h), Image.Resampling.LANCZOS))
            self.canvas.delete("all")
            
            # 2. Image Centering
            self.image_x = (canvas_w - new_w) // 2
            self.image_y = (canvas_h - new_h) // 2
            self.canvas.create_image(self.image_x, self.image_y, image=self.image_tk, anchor=tk.NW)
            
            # 3. Initialize Pivot: SCML Reading and INVERSION
            pivot_x_scml = float(pivot_x_str)
            pivot_y_scml = float(pivot_y_str)
            
            # Invert the SCML Y pivot for visualization (0=top)
            display_pivot_y = 1.0 - pivot_y_scml
            
            # Pivot coordinates on the canvas
            self.pivot_center = (
                self.image_x + new_w * pivot_x_scml,
                self.image_y + new_h * display_pivot_y
            )
            
            self.draw_pivot()
            self.update_pivot_info()
            
        except FileNotFoundError:
            self.image_label.config(text=f"ERROR: File not found in: {image_path}")
        except Exception as e:
            self.image_label.config(text=f"ERROR loading image: {e}")

    # draw_pivot, start_drag, drag, stop_drag, update_pivot_info remain the same
    def draw_pivot(self):
        """Draws the red pivot point on the canvas."""
        self.canvas.delete("pivot")
        r = 5
        x, y = self.pivot_center
        self.pivot_point = self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill='red', outline='white', tags="pivot"
        )
    
    def start_drag(self, event):
        if self.pivot_point in self.canvas.find_closest(event.x, event.y):
            self.canvas.tag_raise(self.pivot_point)
            self._drag_data = {"item": self.pivot_point, "x": event.x, "y": event.y}
        else:
            self._drag_data = None

    def drag(self, event):
        if self._drag_data:
            dx = event.x - self._drag_data["x"]
            dy = event.y - self._drag_data["y"]
            self.canvas.move(self._drag_data["item"], dx, dy)
            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
            
            coords = self.canvas.coords(self.pivot_point)
            self.pivot_center = ((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)
            self.update_pivot_info()

    def stop_drag(self, event):
        self._drag_data = None

    def update_pivot_info(self):
        pivot_x_img = self.pivot_center[0] - self.image_x
        pivot_y_img = self.pivot_center[1] - self.image_y
        
        w_scaled = self.image_tk.width()
        h_scaled = self.image_tk.height()
        
        normalized_x = max(0.0, min(1.0, pivot_x_img / w_scaled)) if w_scaled > 0 else 0.0
        normalized_y = max(0.0, min(1.0, pivot_y_img / h_scaled)) if h_scaled > 0 else 0.0

        self.current_normalized_pivot = (normalized_x, normalized_y)
        self.pivot_info_label.config(text=f"Pivot: X: {normalized_x:.6f}, Y: {normalized_y:.6f}")


    def next_image(self):
        """Saves the current pivot and advances to the next image."""
        global new_pivots
        
        if self.current_image_index < self.total_images:
            file_id, _, _, _ = self.image_data[self.current_image_index]
            new_pivots[file_id] = self.current_normalized_pivot
            
            self.current_image_index += 1
            
            if self.current_image_index < self.total_images:
                self.load_image()
            else:
                self.canvas.delete("all")
                
                finish_text = "Done / Next ChessPiece" if self.manager else "Done and Save"
                self.image_label.config(text=f"All images processed. Press '{finish_text}'.")
                self.next_button["state"] = "disabled"
                self.finish_button["state"] = "normal"
        
        elif self.current_image_index == self.total_images:
             self.finish_editing()


    def finish_editing(self):
        """Finishes editing, applies changes, and advances to the next piece (if in BATCH mode)."""
        global new_pivots
        
        # Save the last image if not done with "Next Image"
        if self.current_image_index == self.total_images - 1 and self.current_normalized_pivot:
            file_id, _, _, _ = self.image_data[self.current_image_index]
            new_pivots[file_id] = self.current_normalized_pivot
        
        # 1. Apply changes to the SCML file
        self.update_scml_file()
        
        # 2. Notify and advance/close
        if self.manager: # BATCH Mode
            self.manager.move_to_next()
        else: # SINGLE Mode
            messagebox.showinfo("Done", "SCML file updated successfully.")
            self.master.destroy()


    def update_scml_file(self):
        """Edits the pivot_x and pivot_y attributes in the SCML file, applying the 1-pivot correction."""
        
        folder_element = self.root.find(f"./folder[@id='0']")
        if folder_element is None:
            return

        for file_id, (pivot_x, pivot_y) in new_pivots.items():
            # PIVOT INTERPRETATION CORRECTION (Y Inversion)
            corrected_pivot_x = pivot_x
            corrected_pivot_y = 1.0 - pivot_y
            # -----------------------------------------------

            file_element = folder_element.find(f"./file[@id='{file_id}']")
            
            if file_element is not None:
                file_element.set('pivot_x', f"{corrected_pivot_x:.6f}")
                file_element.set('pivot_y', f"{corrected_pivot_y:.6f}")
                
        self.tree.write(self.file_path, encoding='UTF-8', xml_declaration=True)


# --- Startup Logic ---

if __name__ == "__main__":
    
    mode, file_list = get_execution_mode()

    if mode == "NONE":
        messagebox.showerror("Execution Error", "Execution mode not found.\n\n"
                             "Run the script:\n"
                             "1. Inside the 'chesspiece_algo/' folder (Single Mode).\n"
                             "2. In the parent directory of the 'exported/' folder (Batch Mode).")
        sys.exit()

    root = tk.Tk()
    
    if mode == "BATCH":
        root.withdraw() # Hide the main window in BATCH mode
        manager = ChessPieceManager(root, file_list)
    else: # mode == "SINGLE"
        scml_path, images_folder = file_list[0]
        app = PivotEditorApp(root, scml_path, images_folder, get_target_image_data(ET.parse(scml_path).getroot()))
        
    root.mainloop()
    sys.exit()