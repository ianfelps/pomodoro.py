#pomodoro clock with py
import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import winsound

# classe principal
class PomodoroTimer:
    def __init__(self):
        # janela tkinter
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        self.root.tk.call('wm', 'iconphoto', self.root._w, PhotoImage(file="tomato.png"))
        self.s = ttk.Style()
        # fonte
        self.s.configure("TNotebook.Tab", font=("Ubuntu", 16))
        self.s.configure("TButton", font=("Ubuntu", 16))
        # abas
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)
        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)
        # tempos
        self.focusPeriod = ttk.Label(self.tab1, text="25:00", font=("Ubuntu", 60))
        self.focusPeriod.pack(pady=20)
        self.shortPause = ttk.Label(self.tab2, text="05:00", font=("Ubuntu", 60))
        self.shortPause.pack(pady=20)
        self.longPause = ttk.Label(self.tab3, text="15:00", font=("Ubuntu", 60))
        self.longPause.pack(pady=20)
        # menu
        self.tabs.add(self.tab1, text=" Período de Foco ")
        self.tabs.add(self.tab2, text=" Pausa Rápida ")
        self.tabs.add(self.tab3, text=" Pausa Longa ")
        # grid
        self.gridLayout = ttk.Frame(self.root)
        self.gridLayout.pack(pady=10)
        # botoes
        self.startButton = ttk.Button(self.gridLayout, text="Iniciar", command=self.startTimerThread)
        self.startButton.grid(row=0, column=0)
        self.skipButton = ttk.Button(self.gridLayout, text="Pular", command=self.skipTimer)
        self.skipButton.grid(row=0, column=1)
        self.resetButton = ttk.Button(self.gridLayout, text="Reiniciar", command=self.resetTimer)
        self.resetButton.grid(row=0, column=2)
        # contador de ciclos
        self.ciclesCounter = ttk.Label(self.gridLayout, text="Ciclos: 0", font=("Ubuntu", 16))
        self.ciclesCounter.grid(row=2, column=0, columnspan=3, pady=5)
        # variaveis
        self.cicles = 0
        self.skipped = False
        self.stopped = False
        self.running = False
        # loop
        self.root.mainloop()

    # começar sequencia de pomodoros
    def startTimerThread(self):
        if not self.running:
            t = threading.Thread(target=self.startTimer)
            t.start()
            self.running = True

    # começar timer
    def startTimer(self):
        # preparando variaveis
        self.skipped = False
        self.stopped = False
        timerId = self.tabs.index(self.tabs.select()) + 1
        # iniciando timer de foco
        if timerId == 1:
            fullSeconds = 25 * 60
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.focusPeriod.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.cicles += 1
                self.ciclesCounter.config(text=f"Ciclos: {self.cicles}")
                if self.cicles % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                for _ in range(2):
                    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
                self.startTimer()
        # iniciando timer de pausa rapida
        elif timerId == 2:
            fullSeconds = 5 * 60
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.shortPause.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                for _ in range(2):
                    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
                self.startTimer()
        # iniciando timer de pausa longa
        elif timerId == 3:
            fullSeconds = 15 * 60
            while fullSeconds > 0 and not self.stopped:
                minutes, seconds = divmod(fullSeconds, 60)
                self.longPause.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                fullSeconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                for _ in range(2):
                    winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
                self.startTimer()
        # erro
        else:
            print("ID de Tempo Inválido!")

    # pular timer
    def skipTimer(self):
        currentTab = self.tabs.index(self.tabs.select())
        if currentTab == 0:
            self.focusPeriod.config(text="25:00")
        elif currentTab == 1:
            self.shortPause.config(text="05:00")
        elif currentTab == 2:
            self.longPause.config(text="15:00")
        self.skipped = True
        self.stopped = True


    # resetar timer
    def resetTimer(self):
        self.stopped = True
        self.skipped = False
        self.running = False
        self.cicles = 0
        self.focusPeriod.config(text="25:00")
        self.shortPause.config(text="05:00")
        self.longPause.config(text="15:00")
        self.ciclesCounter.config(text="Ciclos: 0")

PomodoroTimer()