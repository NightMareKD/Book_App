import tkinter as tk
from tkinter import ttk, messagebox
from database import get_books, update_page, add_book
from utils import export_stats_to_csv

class BookKeeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 BookKeeper - Reading Progress Tracker")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a2332")  # Dark blue background
        
        # Configure custom style
        self.setup_styles()
        
        self.book_frames = []
        self.selected_book_id = None
        self.selected_frame = None
        
        # Create main header
        self.create_header()
        
        # Create scrollable books container
        self.create_books_container()
        
        # Create control panel
        self.create_control_panel()
        
        self.refresh_books()

    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        
        # Configure progress bar style
        style.configure("Custom.Horizontal.TProgressbar",
                       background="#ff7f00",  # Orange
                       troughcolor="#2d3748",
                       borderwidth=0,
                       lightcolor="#ff7f00",
                       darkcolor="#ff7f00")

    def create_header(self):
        """Create the application header"""
        header_frame = tk.Frame(self.root, bg="#1a2332", height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, 
                              text="📚 BookKeeper", 
                              font=("Arial", 24, "bold"),
                              fg="#ff7f00",  # Orange
                              bg="#1a2332")
        title_label.pack(side=tk.TOP)
        
        subtitle_label = tk.Label(header_frame,
                                 text="Track Your Reading Progress",
                                 font=("Arial", 12),
                                 fg="#94a3b8",  # Light gray
                                 bg="#1a2332")
        subtitle_label.pack(side=tk.TOP)

    def create_books_container(self):
        """Create scrollable container for books"""
        # Main container frame
        container_frame = tk.Frame(self.root, bg="#1a2332")
        container_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas and scrollbar for scrolling
        canvas = tk.Canvas(container_frame, bg="#1a2332", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=canvas.yview)
        self.books_container = tk.Frame(canvas, bg="#1a2332")
        
        self.books_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.books_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_control_panel(self):
        """Create the control panel with buttons and inputs"""
        control_frame = tk.Frame(self.root, bg="#2d3748", relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Selected book indicator
        self.selected_label = tk.Label(control_frame,
                                      text="Select a book to update progress",
                                      font=("Arial", 10, "italic"),
                                      fg="#94a3b8",
                                      bg="#2d3748")
        self.selected_label.pack(pady=(10, 5))
        
        # Page update section
        page_frame = tk.Frame(control_frame, bg="#2d3748")
        page_frame.pack(pady=5)
        
        tk.Label(page_frame, text="Current Page:", 
                font=("Arial", 10, "bold"),
                fg="#e2e8f0", bg="#2d3748").pack(side=tk.LEFT, padx=(0, 5))
        
        self.page_entry = tk.Entry(page_frame, 
                                  font=("Arial", 10),
                                  width=10,
                                  bg="#1a2332",
                                  fg="#e2e8f0",
                                  insertbackground="#ff7f00",
                                  relief=tk.FLAT,
                                  bd=5)
        self.page_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        update_btn = tk.Button(page_frame, 
                              text="Update Progress",
                              command=self.update_page,
                              bg="#ff7f00",
                              fg="white",
                              font=("Arial", 10, "bold"),
                              relief=tk.FLAT,
                              padx=20,
                              cursor="hand2")
        update_btn.pack(side=tk.LEFT)
        
        # Button row
        button_frame = tk.Frame(control_frame, bg="#2d3748")
        button_frame.pack(pady=(5, 15))
        
        add_btn = tk.Button(button_frame,
                           text="📖 Add New Book",
                           command=self.add_new_book,
                           bg="#1a2332",
                           fg="#ff7f00",
                           font=("Arial", 10, "bold"),
                           relief=tk.FLAT,
                           padx=20,
                           pady=5,
                           cursor="hand2")
        add_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        export_btn = tk.Button(button_frame,
                              text="📊 Export Stats",
                              command=self.export_stats,
                              bg="#1a2332",
                              fg="#94a3b8",
                              font=("Arial", 10, "bold"),
                              relief=tk.FLAT,
                              padx=20,
                              pady=5,
                              cursor="hand2")
        export_btn.pack(side=tk.LEFT)

    def clear_book_frames(self):
        """Clear all book frames"""
        for frame in self.book_frames:
            frame.destroy()
        self.book_frames = []

    def refresh_books(self):
        """Refresh the books display"""
        self.clear_book_frames()
        books = get_books()
        
        if not books:
            # Show empty state
            empty_frame = tk.Frame(self.books_container, bg="#1a2332")
            empty_frame.pack(fill=tk.X, pady=50)
            
            empty_label = tk.Label(empty_frame,
                                  text="📚 No books yet!\nClick 'Add New Book' to get started",
                                  font=("Arial", 14),
                                  fg="#94a3b8",
                                  bg="#1a2332",
                                  justify=tk.CENTER)
            empty_label.pack()
            
            self.book_frames.append(empty_frame)
            return
        
        for book in books:
            book_id, title, total_pages, current_page = book
            progress = int((current_page / total_pages) * 100) if total_pages else 0
            
            # Main book frame
            frame = tk.Frame(self.books_container, 
                           bg="#2d3748", 
                           relief=tk.RAISED, 
                           bd=2,
                           padx=15, 
                           pady=15)
            frame.pack(fill=tk.X, pady=8)
            
            # Hover effects
            def on_enter(e, f=frame):
                if f != self.selected_frame:
                    f.configure(bg="#374151")
            
            def on_leave(e, f=frame):
                if f != self.selected_frame:
                    f.configure(bg="#2d3748")
            
            def select_book(e, bid=book_id, f=frame):
                # Reset previous selection
                if self.selected_frame:
                    self.selected_frame.configure(bg="#2d3748")
                
                # Set new selection
                self.selected_book_id = bid
                self.selected_frame = f
                f.configure(bg="#1e40af")  # Darker blue for selection
                
                # Update selected book label
                book_title = title if len(title) <= 30 else title[:30] + "..."
                self.selected_label.configure(
                    text=f"Selected: {book_title}",
                    fg="#ff7f00"
                )
            
            frame.bind("<Button-1>", select_book)
            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)
            
            # Book title
            title_display = title if len(title) <= 40 else title[:40] + "..."
            title_lbl = tk.Label(frame, 
                               text=title_display,
                               font=("Arial", 14, "bold"),
                               fg="#e2e8f0",
                               bg="#2d3748")
            title_lbl.pack(anchor="w", pady=(0, 8))
            title_lbl.bind("<Button-1>", select_book)
            
            # Progress bar
            progress_frame = tk.Frame(frame, bg="#2d3748")
            progress_frame.pack(fill=tk.X, pady=(0, 8))
            
            bar = ttk.Progressbar(progress_frame, 
                                length=350, 
                                mode='determinate',
                                style="Custom.Horizontal.TProgressbar")
            bar['value'] = progress
            bar.pack(side=tk.LEFT)
            
            progress_text = tk.Label(progress_frame,
                                   text=f"{progress}%",
                                   font=("Arial", 10, "bold"),
                                   fg="#ff7f00",
                                   bg="#2d3748")
            progress_text.pack(side=tk.RIGHT, padx=(10, 0))
            
            # Page info
            page_info = tk.Frame(frame, bg="#2d3748")
            page_info.pack(fill=tk.X)
            
            page_lbl = tk.Label(page_info,
                              text=f"Progress: {current_page} / {total_pages} pages",
                              font=("Arial", 10),
                              fg="#94a3b8",
                              bg="#2d3748")
            page_lbl.pack(side=tk.LEFT, anchor="w")
            page_lbl.bind("<Button-1>", select_book)
            
            remaining_pages = total_pages - current_page
            if remaining_pages > 0:
                remaining_lbl = tk.Label(page_info,
                                       text=f"{remaining_pages} pages left",
                                       font=("Arial", 10, "italic"),
                                       fg="#64748b",
                                       bg="#2d3748")
                remaining_lbl.pack(side=tk.RIGHT)
                remaining_lbl.bind("<Button-1>", select_book)
            
            self.book_frames.append(frame)

    def update_page(self):
        """Update the current page for selected book"""
        if not self.selected_book_id:
            messagebox.showwarning("No Book Selected", 
                                 "Please select a book first by clicking on it.")
            return
        
        try:
            page = int(self.page_entry.get())
            if page < 0:
                messagebox.showerror("Invalid Input", 
                                   "Page number cannot be negative.")
                return
            
            update_page(self.selected_book_id, page)
            self.page_entry.delete(0, tk.END)
            self.refresh_books()
            messagebox.showinfo("Success", "Progress updated successfully!")
            
        except ValueError:
            messagebox.showerror("Invalid Input", 
                               "Please enter a valid page number.")

    def add_new_book(self):
        """Open dialog to add a new book"""
        new_window = tk.Toplevel(self.root)
        new_window.title("Add New Book")
        new_window.geometry("400x300")
        new_window.configure(bg="#1a2332")
        new_window.resizable(False, False)
        
        # Center the window
        new_window.transient(self.root)
        new_window.grab_set()
        
        # Header
        header = tk.Label(new_window,
                         text="📖 Add New Book",
                         font=("Arial", 18, "bold"),
                         fg="#ff7f00",
                         bg="#1a2332")
        header.pack(pady=(20, 30))
        
        # Form frame
        form_frame = tk.Frame(new_window, bg="#1a2332")
        form_frame.pack(padx=40, pady=20, fill=tk.BOTH, expand=True)
        
        # Title field
        tk.Label(form_frame, text="Book Title:",
                font=("Arial", 12, "bold"),
                fg="#e2e8f0", bg="#1a2332").pack(anchor="w", pady=(0, 5))
        
        title_entry = tk.Entry(form_frame,
                              font=("Arial", 12),
                              bg="#2d3748",
                              fg="#e2e8f0",
                              insertbackground="#ff7f00",
                              relief=tk.FLAT,
                              bd=5)
        title_entry.pack(fill=tk.X, pady=(0, 20))
        title_entry.focus()
        
        # Total pages field
        tk.Label(form_frame, text="Total Pages:",
                font=("Arial", 12, "bold"),
                fg="#e2e8f0", bg="#1a2332").pack(anchor="w", pady=(0, 5))
        
        total_entry = tk.Entry(form_frame,
                              font=("Arial", 12),
                              bg="#2d3748",
                              fg="#e2e8f0",
                              insertbackground="#ff7f00",
                              relief=tk.FLAT,
                              bd=5)
        total_entry.pack(fill=tk.X, pady=(0, 30))
        
        def save_book():
            try:
                title = title_entry.get().strip()
                pages = int(total_entry.get())
                
                if not title:
                    messagebox.showerror("Invalid Input", "Please enter a book title.")
                    return
                
                if pages <= 0:
                    messagebox.showerror("Invalid Input", 
                                       "Total pages must be greater than 0.")
                    return
                
                add_book(title, pages)
                new_window.destroy()
                self.refresh_books()
                messagebox.showinfo("Success", f"'{title}' added successfully!")
                
            except ValueError:
                messagebox.showerror("Invalid Input", 
                                   "Please enter a valid number for total pages.")
        
        def cancel():
            new_window.destroy()
        
        # Buttons
        button_frame = tk.Frame(form_frame, bg="#1a2332")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        cancel_btn = tk.Button(button_frame,
                              text="Cancel",
                              command=cancel,
                              bg="#64748b",
                              fg="white",
                              font=("Arial", 12, "bold"),
                              relief=tk.FLAT,
                              padx=30,
                              pady=8,
                              cursor="hand2")
        cancel_btn.pack(side=tk.RIGHT)
        
        save_btn = tk.Button(button_frame,
                            text="Add Book",
                            command=save_book,
                            bg="#ff7f00",
                            fg="white",
                            font=("Arial", 12, "bold"),
                            relief=tk.FLAT,
                            padx=30,
                            pady=8,
                            cursor="hand2")
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Enter key binding
        new_window.bind('<Return>', lambda e: save_book())

    def export_stats(self):
        """Export statistics with user feedback"""
        try:
            export_stats_to_csv()
            messagebox.showinfo("Export Successful", 
                              "Statistics exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Failed", 
                               f"Failed to export statistics: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookKeeperApp(root)
    root.mainloop()