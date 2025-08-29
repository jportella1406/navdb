def apply_styles(ttk):
    style = ttk.Style()
    style.theme_use('clam')

    style.configure("Rounded.TButton",
                    background="#2980b9",
                    foreground="white",
                    font=("Segoe UI", 10, "bold"),
                    padding=10,
                    borderwidth=0,
                    relief="flat")

    style.map("Rounded.TButton",
              background=[("active", "#3498db")],
              foreground=[("disabled", "gray")])

    style.configure("TFrame", background="#f4f4f4")
    style.configure("TLabel", background="#f4f4f4", foreground="#2c3e50", font=("Segoe UI", 10))
    style.configure("TButton", background="#2980b9", foreground="white", font=("Segoe UI", 10, "bold"))
    style.map("TButton",
              background=[("active", "#3498db")],
              foreground=[("disabled", "gray")])
