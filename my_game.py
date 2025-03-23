from pickle import*
from tkinter import *
from pygame import *
from random import choice
import mymodule as m
from webbrowser import open_new

r = ['accurate', 'appropriate', 'equitable', 'exact', 'factual', 'legitimate', 'perfect', 'precise', 'proper', 'strict', 'true', 'okay', 'right', 'stone', 'actual', 'faultless', 'flawless', 'for sure', 'free of error', 'impeccable', 'just', 'nice', 'on the ball', 'on the beam', 'on the button', 'on the money', 'on the nose', 'on track', 'on-target', 'regular', 'right as rain']
score =0
a = 'a'
b = []
mixer.init()
correct = mixer.Sound("jump.wav")
wrong= mixer.Sound('die.wav')
bgsound=mixer.Sound('game bg.mp3')

class StartMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title('Start Menu')
        self.geometry('600x600')
        self.resizable(False, False)

        

        new_game = Button(self, text='Start Game', font=('Arial', 20),width=14, height=1,fg='white', bg='#ff7b3f', command=self.start)
        new_game.pack()
        new_game.place(relx=0.275, rely=0.748, anchor='center')



        highscore = Button(self, text='High Score', font=('Helvetica', 20),width=11,fg='white', bg='#04b5dc', command=self.show_high_score)
        highscore.pack()
        highscore.place(relx=0.76, rely=0.748, anchor='center')

        quitbt = Button(self, text='Terminate', font=('Helvetica', 20),bg='#04b5dc', fg = 'white',width=12, command=self.quit_game)
        quitbt.pack()
        quitbt.place(relx=0.745, rely=0.896, anchor='center')

        meanin= Button(self, text=f'New word' ,bg='#ff7b3f', fg = 'white',width=12,font=('Helvetica', 20))
        meanin.pack()
        meanin.place(relx=0.245, rely=0.896, anchor='center')
        def meaning():
            url = f"https://www.dictionary.com/browse/"
            open_new(url)
        meanin.config(command=meaning)

        self.bg_image = PhotoImage(file="start.png")
        bg_label = Label(self, image=self.bg_image)
        bg_label.image = self.bg_image  # Keep a reference to the image to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()


    def level(self):
        global w, t
        lev = Tk()
        lev.geometry('405x720')
        lev.resizable(False, False)

        def easy_lev():
            global w, t
            w = 2
            t = 30
            lev.destroy()
            self.start_game()

        def med_lev():
            global w, t
            w = 3
            t = 20
            lev.destroy()
            self.start_game()

        def hard_lev():
            global w, t
            w = 4
            t = 10
            lev.destroy()
            self.start_game()

        bg_image = PhotoImage(file="background.png")
        bg_label = Label(lev, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)            

        label = Label(lev, text='Choose Difficulty Level', font=('Arial Black', 18),bg='#0C1A27',fg='white')
        label.pack()
        label.place(relx=0.5, rely=0.05, anchor='center')

        easy = Button(lev, text='Easy', font=('Helvetica', 14), command=easy_lev)
        easy.pack()
        easy.place(relx=0.5, rely=0.5, anchor='center')

        med = Button(lev, text='Medium', font=('Helvetica', 14), command=med_lev)
        med.pack()
        med.place(relx=0.5, rely=0.6, anchor='center')

        hard = Button(lev, text='Hard', font=('Helvetica', 14), command=hard_lev)
        hard.pack()
        hard.place(relx=0.5, rely=0.7, anchor='center')

        lev.mainloop()

        

        
    def start(self):
        self.destroy()
        self.level()
        
    def start1(self):
        global game
        game.destroy() 
        self.start_game()
        
    def mainmenu(self):
        global game
        game.destroy()
        self.__init__()

    def start_game(self):
        global game
        game = Tk()
        game.title('Word game')
        game.geometry('600x600')
        game.resizable(False, False)
        ai=None
        bgsound.play()
        time=10

        
        meanin= Button(game, text=f'Meaning' ,bg='blue', fg = 'white',font=('Helvetica', 14))

        
        
        def display_error_message(message):
             global score ,ai,a,b,score
             error_message.config(text=message, fg='red', bg='black')
             error_message.pack()
             error_message.place(relx=0.5, rely=0.38, anchor='center')
             submit_button.destroy()
             label.destroy()
             entry.destroy()
             meanin.destroy()
             score_label.destroy()
             bg_label.destroy()
             game.geometry('400x300')
             game.resizable(False, False)
             game.configure(bg='black')
             quit_button.destroy()
             result_label.destroy()
             wrong.play()
             bgsound.stop()
             a = 'a'
             b = []
             with open('highscores.dat', 'rb+') as f:
                 x = load(f)
                 x.append(score)
                 x.sort(reverse=True)
                 f.seek(0)   
                 dump(x,f)

             score =0
             restart= Button(game,text='Restart', font=('Helvetica', 15), command=self.start1)
             restart.pack()
             restart.place(relx=0.5, rely=0.75, anchor='center')
             
             main= Button(game,text='Main Menu', font=('Helvetica', 15), command=self.mainmenu)
             main.pack()
             main.place(relx=0.5, rely=0.9, anchor='center')
            
        def validate_word(event=None):
              nonlocal ai  , meanin , time
              global a, b, score,correct
              if ai is not None:
                game.after_cancel(ai)
              x = entry.get().lower()
              if x == '':
                display_error_message(f'Empty string \n Game over!\n Thanks for playing \n Score:{score}')
              elif x[0] != a[-1]:
                display_error_message(f"Word doesn't start with {a[-1]}\n Game over!\n Thanks for playing\n Score:{score}")
              elif len(x) < w:
                   display_error_message(f"Word doesn't have more than {w} letters\n Game over!\n Thanks for playing\n Score:{score}")
              elif x in b:
                   display_error_message(f"{x} is a repeated word\n Game over!\n Thanks for playing\n Score:{score}")
              elif x not in m.word_set():
                   display_error_message(f"{x} is not a valid English word\n Game over!\n Thanks for playing\n Score:{score}")
              else:
                    b.append(x)
                    a = x
                    entry.delete(0, END)
                    label.config(text=f"Enter a {w} or more letter word starting with '{a[-1]}' in {t} second:")
                    result_label.config(text=choice(r))
                    score += 1
                    score_label.config(text=f"Score: {score}")
                    correct.play()
                    ai = game.after(t*1000, lambda: display_error_message(f"Time over\n Thanks for playing \n Score:{score}"))
                    meanin.destroy()
                    meanin= Button(game, text=f'Meaning of {x}' ,bg='#182142', fg = 'white',font=('Helvetica', 20))
                    meanin.pack()
                    meanin.place(relx=0.5, rely=0.915, anchor='center')
                    def meaning():
                       nonlocal x
                       game.after_cancel(ai)
                       url = f"https://www.dictionary.com/browse/{x}"
                       open_new(url)  
                    meanin.config(command=meaning)
                    

        bg_image = PhotoImage(file="bg.png")
        bg_label = Label(game, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        label = Label(game, text=f"Enter a {w} or more letter word starting with '{a[-1]}'", font=('Arial Black', 11),bg='#192243',fg='white')
        label.pack()
        label.place(relx=0.5, rely=0.7, anchor='center')

        entry = Entry(game, font=('Helvetica', 20),width=30)
        entry.pack()
        entry.place(relx=0.5, rely=0.6, anchor='center')
        entry.focus

        result_label = Label(game, text="", font=('Arial Black', 14),bg='#120823',fg='white')
        result_label.pack()
        result_label.place(relx=0.8, rely=0.05, anchor='center')

        submit_button = Button(game, text="Submit", font=('Helvetica', 21), command=validate_word,width=13,height=1,bg='#fafafb')
        submit_button.pack()
        submit_button.place(relx=0.31, rely=0.78, anchor='center')
        game.bind('<Return>', validate_word)
        
        score_label = Label(game, text=f"Score: {score}", font=('Helvetica', 14),bg='#120823',fg='white')
        score_label.pack(pady=10)
        score_label.place(relx=0.1, rely=0.05, anchor='center')

        error_message = Label(game, text="", font=('Helvetica', 17))
        
        
        def quit_game(event=None):
           game.destroy()

        quit_button = Button(game, text="  Quit Game  ", font=('Helvetica', 20),bg='#22345c', fg = 'white', command=quit_game,width=11)
        quit_button.pack(pady=20)
        quit_button.place(relx=0.56, rely=0.734)
        game.bind('<Escape>', quit_game)

        
        
        game.mainloop()


    def show_high_score(self):
        highscore_window = Tk()
        highscore_window.title('High Scores')
        highscore_window.geometry('400x300')
        highscore_window.resizable(False, False)
        highscore_window.configure(bg='black')

        with open('highscores.dat', 'rb') as f:
            score = load(f)
            score=score[:3]

        scores_label = Label(highscore_window, text='High Scores', font=('Helvetica', 25),fg='gold',bg='black')
        scores_label.pack()
        scores_label.place(relx=0.5, rely=0.1, anchor='center')

        scores_text = '\n'.join(map(str, score))
        scores_label = Label(highscore_window, text=scores_text, font=('Helvetica', 18),fg='gold',bg='black')
        scores_label.pack(pady=20)
        scores_label.place(relx=0.5, rely=0.5, anchor='center')

        close_button = Button(highscore_window, text='Close', font=('Helvetica', 14), command=highscore_window.destroy)
        close_button.pack()
        close_button.place(relx=0.5, rely=0.9, anchor='center')

        highscore_window.mainloop()

    def quit_game(self):
        self.destroy()

    def creator(self):
        url = f"https://wordbuilding2.wordpress.com/2023/07/16/wordbuilding/"
        open_new(url)


        
            
        
if __name__ == '__main__' :
    
    start_menu = StartMenu()
    start_menu.mainloop()
