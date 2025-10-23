import tkinter
import determineFeatures_loadData as dl
import gui

if __name__ == "__main__":
    words = dl.load_words()
    root = tkinter.Tk()
    app = gui.WordleApp(root, words)
    root.mainloop()