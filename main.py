import time
import random
from tkinter import font
from tkinter import *
from tkinter import messagebox

alert = messagebox.showinfo


SHOW_TOPBAR = True


class CowsAndBulls:
    def __init__(self):
        self.window = Tk()
        self.window.title('Быки и коровы')
        self.init_frame_and_buttons()
        self.init_menu()
        self.make_full_screen()

    def init_menu(self):
        menubar = Menu(self.window)

        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label='Игрок с компьютером',
                             command=self.start_game, accelerator='N')
        filemenu.add_command(
            label='Выйти', command=self.quitwin, accelerator='Escape')
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label='Правила', command=self.show_help)
        helpmenu.add_command(label='Об игре', command=self.show_credits)

        menubar.add_cascade(label='Меню', menu=filemenu)
        menubar.add_cascade(label='Помощь', menu=helpmenu)

        self.window.config(menu=menubar)

    def make_full_screen(self):
        root = self.window

        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.overrideredirect(not SHOW_TOPBAR)
        root.geometry("%dx%d+0+0" % (width, height))

    def init_frame(self):
        try:
            self.frame.destroy()
        except:
            pass

        self.frame = Frame(self.window)
        self.frame.pack()

    def init_frame_and_buttons(self):
        self.init_frame()
        listOfButtons = []
        self.big = font.Font(family='helvetica', size=24)

        listOfButtons.append(
            Button(self.frame, text='Игра с компьютером', command=self.start_game))
        listOfButtons.append(
            Button(self.frame, text='Рекорды', command=self.see_records))
        listOfButtons.append(
            Button(self.frame, text='Выйти', command=self.quitwin))

        for button in range(len(listOfButtons)):
            listOfButtons[button]['font'] = self.big
            listOfButtons[button].pack(side='top')

    def start_game(self):
        target = ''
        target += str(random.choice(range(1, 10, 1)))

        for _ in range(3):
            target += str(random.choice(range(10)))

        target = int(target)

        self.init_frame()
        self.frame.grid()

        frame = self.frame

        global counter

        counter = 1

        Label(frame, text='Число', width=15).grid(row=counter, column=1)
        Label(frame, text='Быки', width=15).grid(row=counter, column=2)
        Label(frame, text='Коровы', width=15).grid(row=counter, column=3)

        counter += 1

        a = StringVar()

        def validate():
            flag = True
            guess = str(a.get())

            if not (len(guess) == 4):
                alert('Ошибка', 'Введите четырёхзначное число')
                flag = False

            else:
                try:
                    int(guess)
                except:
                    alert('Ошибка', 'Ввести можно только четырёхзначное число')
                    flag = False

            if flag:
                done()

        def done():
            guess = str(a.get())
            bulls = 0
            cows = 0

            bulls, cows = bulls_and_cows(guess, target)

            if str(a.get()) == str(target):
                self.over_game()

            global counter

            Label(frame, text=str(a.get())).grid(row=counter, column=1)
            Label(frame, text=str(bulls)).grid(row=counter, column=2)
            Label(frame, text=str(cows)).grid(row=counter, column=3)

            counter += 1

            a.set('')

        def digits(number):
            return [int(d) for d in str(number)]

        def bulls_and_cows(guess, target):
            guess, target = digits(guess), digits(target)
            bulls = [d1 == d2 for d1, d2 in zip(guess, target)].count(True)
            cows = 0

            for digit in set(guess):

                cows += min(guess.count(digit), target.count(digit))

            return bulls, cows - bulls

        d = Entry(frame, textvariable=a, width=4)

        d.grid(row=0, column=0)
        d.focus()

        self.window.bind('<Return>', validate)

        Button(frame, text='Угадать', command=validate).grid(row=0, column=1)
        Button(frame, text='Завершить игру', command=self.ask_game_end).grid(
            row=0, column=2)
        Button(frame, text='Меню', command=self.init_frame_and_buttons).grid(
            row=0, column=3)

    def ask_game_end(self):

        if messagebox.askyesno('Вы уверены?', 'Точно закончить игру?', icon='warning'):

            self.win('c')
            self.init_frame_and_buttons()

        else:

            return

    def over_game(self):
        alert('Игра завершена', 'Победил игрок')
        self.win('u')
        self.init_frame_and_buttons()

    def win(self, param):
        form = '%B %d, %Y, %H:%M:%S'
        filin = open('records.txt', 'a')
        filin.write(time.strftime(form) + '|')

        if param == 'c':
            filin.write('Компьютер')

        if param == 'u':
            filin.write('Игрок')

        filin.write('\n')
        filin.close()

    def see_records(self):
        a = open('records.txt', 'r')
        a.seek(0)
        b = Toplevel()
        f = Frame(b)
        f.grid()

        Label(f, text="Дата", fg='red', bg='black',
              width=25).grid(row=0, column=0)
        Label(f, text="Победитель", fg='red', bg='black',
              width=25).grid(row=0, column=2)

        counter = 1

        if len(a.readlines()) == 0:
            alert('Рекордов пока нет', 'Рекордов ещё не было')
            return

        a.seek(0)

        for i in a:
            date, winner = i.split('|')
            Label(f, text=date).grid(row=counter, column=0)
            Label(f, text=winner).grid(row=counter, column=2)
            counter += 1

        Button(f, command=b.destroy, text="Выйти").grid(
            row=counter+1, column=1)

    def show_help(self):
        alert('Правила', """Противники по очереди называют друг другу числа и сообщают о количестве
«быков» и «коров» в названном числе («бык» — цифра есть в записи
задуманного числа и стоит в той же позиции, что и в задуманном числе;
«корова» — цифра есть в записи задуманного числа, но не стоит в той же
позиции, что и в задуманном числе).
Например, если задумано число 3275 и названо число 1234, получаем в
названном числе одного «быка» и одну «корову». Очевидно, что число
отгадано в том случае, если имеем 4 «быка».""")

    def show_credits(self):
        toplevel = Toplevel()

        Label(toplevel, text='Быки и коровы',
              font=self.big).grid(row=0, column=0)
        Label(toplevel, text='Написано на python и tkinter',
              font=self.big).grid(row=1, column=0)
        Button(toplevel, text="Выйти", command=toplevel.destroy).grid(
            row=2, column=0)

    def quitwin(self):
        try:
            self.window.destroy()
            self.init_frame()
            self.frame.grid()
            self.frame.grid_propagate(1)
            self.big = font.Font(family='helvetica', size=24)
            r = self.frame

            Label(r, text='Быки и коровы',
                  font=self.big).grid(row=0, column=0)

            self.window.after(8000, self.window.destroy)
        except:
            pass


def main():
    CowsAndBulls()
    mainloop()


if __name__ == '__main__':
    main()
