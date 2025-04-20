import tkinter as tk
from tkinter import ttk
import threading

_connection_window = None
_window_open = False 
_close_event = threading.Event()

def show_connection_window(code):
    global _connection_window, _window_open, _close_event

    if _window_open:
        return

    def create_window():
        global _connection_window, _window_open
        _close_event.clear()

        try:
            _connection_window = tk.Tk()
        except Exception as e:
            print("Error creating Tk window:", e)
            return

        _connection_window.title("Silicore Client - Bağlantı Bekleniyor")
        _connection_window.geometry("500x350")
        _connection_window.resizable(False, False)

        # Stil
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 12), padding=10)
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Hint.TLabel", font=("Segoe UI", 10), foreground="#555")

        main_frame = ttk.Frame(_connection_window, padding=20)
        main_frame.pack(fill="both", expand=True)

        label = ttk.Label(main_frame, text="Eşleştirme Kodu:", style="TLabel")
        label.pack()

        code_label = ttk.Label(main_frame, text=code, style="Header.TLabel", foreground="#2E86AB")
        code_label.pack(pady=(0, 10))

        waiting_label = ttk.Label(main_frame, text="Telefon uygulamasından bu kod ile bağlanın.", style="Hint.TLabel")
        waiting_label.pack()

        long_text = "Bu arayüz telefona bağlandığınız zaman bir sonraki kontrolde kendiliğinden kapanır. Bağlantı kesildiğinde ise tekrar açılır."
        explanation_label = ttk.Label(main_frame, text=long_text, style="Hint.TLabel", wraplength=460) 
        explanation_label.pack()

        label_first = ttk.Label(main_frame, text="Silicore Client", font=("Segoe UI", 10,"bold"), foreground="#555")
        label_first.pack()

        _connection_window.protocol("WM_DELETE_WINDOW", close_connection_window)
        _window_open = True

        def check_close():
            if _close_event.is_set():
                _connection_window.destroy()
                return
            _connection_window.after(100, check_close)

        _connection_window.after(100, check_close)

        try:
            _connection_window.mainloop()
        except Exception as e:
            print("Mainloop error:", e)
        finally:
            _window_open = False

    threading.Thread(target=create_window, daemon=True).start()

def close_connection_window():
    global _connection_window, _window_open, _close_event
    _close_event.set()
    try:
        if _connection_window is not None:
            _connection_window.after(0, _connection_window.destroy)
    except tk.TclError:
        pass
    _window_open = False
    _connection_window = None

def is_window_open():
    global _window_open
    return _window_open
