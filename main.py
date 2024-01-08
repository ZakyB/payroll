from views.main_window import MainWindow

def main():
    root = MainWindow()
    root.update_views()
    root.mainloop()

if __name__ == "__main__":
    main()