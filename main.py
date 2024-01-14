import time
import random
from tkinter import font
from tkinter import *
from tkinter import messagebox, Entry, Tk

alert = messagebox.showinfo


SHOW_TOP_BAR = True


class CowsAndBulls:
    is_one_player = True
    first_number = None
    second_number = None
    is_first_player = True

    def __init__(self):
        self.window = Tk()
        try:
            self.window.iconphoto(False, PhotoImage(file='icon.png'))
        except:
            pass
        self.window.title('Быки и коровы')
        self.init_frame_and_buttons()
        self.init_menu()
        self.window.eval('tk::PlaceWindow . center')

    def init_menu(self):
        menubar = Menu(self.window)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label='Игрок с компьютером',
                              command=self.start_ai_game)
        file_menu.add_command(label='Два игрока',
                              command=self.start_two_players_game)
        file_menu.add_command(
            label='Выйти', command=self.quitwin)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label='Правила', command=self.show_help)
        help_menu.add_command(label='Об игре', command=self.show_credits)

        menubar.add_cascade(label='Меню', menu=file_menu)
        menubar.add_cascade(label='Помощь', menu=help_menu)

        self.window.config(menu=menubar)

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
            Button(self.frame, text='Игрок с компьютером', command=self.start_ai_game))
        listOfButtons.append(
            Button(self.frame, text='Два игрока', command=self.start_two_players_game))
        listOfButtons.append(
            Button(self.frame, text='Рекорды', command=self.show_records))
        listOfButtons.append(
            Button(self.frame, text='Выйти', command=self.quitwin))

        for button in range(len(listOfButtons)):
            listOfButtons[button]['font'] = self.big
            listOfButtons[button].pack(side='top')

    def start_ai_game(self):
        self.is_one_player = True

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

        user_input = StringVar()

        def validate():
            flag = True
            guess = str(user_input.get())

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
            guess = str(user_input.get())
            bulls = 0
            cows = 0

            bulls, cows = bulls_and_cows(guess, target)

            if user_input.get() == str(target):
                self.over_game()

            global counter

            Label(frame, text=str(user_input.get())).grid(
                row=counter, column=1)
            Label(frame, text=str(bulls)).grid(row=counter, column=2)
            Label(frame, text=str(cows)).grid(row=counter, column=3)

            counter += 1

            user_input.set('')

        def digits(number):
            return [int(d) for d in str(number)]

        def bulls_and_cows(guess, target):
            guess, target = digits(guess), digits(target)
            bulls = [d1 == d2 for d1, d2 in zip(guess, target)].count(True)
            cows = 0

            for digit in set(guess):

                cows += min(guess.count(digit), target.count(digit))

            return bulls, cows - bulls

        entry = Entry(frame, textvariable=user_input, width=4)
        entry.grid(row=0, column=0)
        entry.focus()

        self.window.bind('<Return>', validate)

        Button(frame, text='Угадать', command=validate).grid(row=0, column=1)
        Button(frame, text='Завершить игру', command=self.ask_game_end).grid(
            row=0, column=2)
        Button(frame, text='Меню', command=self.init_frame_and_buttons).grid(
            row=0, column=3)

    def get_user_number(self, player_title, is_first):
        try:
            player_window = Tk()
            player_window.eval(f'tk::PlaceWindow . center')
            player_window.title(player_title)

            player_entry = Entry(
                player_window,
                show='*',
                width=64
            )
            player_entry.pack(pady=10)

            def save_number():
                number = player_entry.get()
                if number.isdigit() and len(number) == 4:
                    if is_first:
                        self.first_number = number
                    else:
                        self.second_number = number

                    player_window.quit()
                    player_window.destroy()
                else:
                    messagebox.showerror(
                        'Ошибка', 'Число должно быть четырёхзначным и состоять из цифр')

            submit_button = Button(
                player_window, text="Загадать", command=save_number)
            submit_button.pack()
            player_window.mainloop()
        except:
            messagebox.showerror('Ошибка', 'Что-то пошло не так')

    def start_two_players_game(self):
        self.is_one_player = False

        self.get_user_number(
            "Первый игрок вводит четырёхзначное число", is_first=True)
        self.get_user_number(
            "Второй игрок вводит четырёхзначное число", is_first=False)

        self.run_two_players_game()

    def run_two_players_game(self):
        self.is_first_player = True

        first_number = self.first_number
        second_number = self.second_number

        self.init_frame()
        self.frame.grid()
        frame = self.frame

        global counter
        counter = 1

        Label(frame, text='Игрок', width=15).grid(row=counter, column=1)
        Label(frame, text='Число', width=15).grid(row=counter, column=2)
        Label(frame, text='Быки', width=15).grid(row=counter, column=3)
        Label(frame, text='Коровы', width=15).grid(row=counter, column=4)

        counter += 1

        user_input = StringVar()

        def validate():
            flag = True
            guess = str(user_input.get())

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
            guess = str(user_input.get())
            bulls = 0
            cows = 0

            number = second_number if self.is_first_player else first_number

            bulls, cows = bulls_and_cows(guess, number)
            player_label = 'Первый игрок' if self.is_first_player else 'Второй игрок'

            if str(user_input.get()) == number:
                self.over_game(player_label)

            global counter

            try:
                Label(frame, text=player_label).grid(
                    row=counter, column=1)
                Label(frame, text=str(user_input.get())).grid(
                    row=counter, column=2)
                Label(frame, text=str(bulls)).grid(row=counter, column=3)
                Label(frame, text=str(cows)).grid(row=counter, column=4)
            except:
                pass

            counter += 1

            self.is_first_player = not self.is_first_player
            user_input.set('')

        def digits(number):
            return [int(d) for d in str(number)]

        def bulls_and_cows(guess, target):
            guess, target = digits(guess), digits(target)
            bulls = [d1 == d2 for d1, d2 in zip(guess, target)].count(True)
            cows = 0

            for digit in set(guess):
                cows += min(guess.count(digit), target.count(digit))

            return bulls, cows - bulls

        entry = Entry(frame, textvariable=user_input, width=4)
        entry.grid(row=0, column=0)
        entry.focus()

        self.window.bind('<Return>', validate)

        Button(frame, text='Угадать', command=validate).grid(
            row=0, column=1)
        Button(frame, text='Завершить игру', command=self.ask_game_end).grid(
            row=0, column=2)
        Button(frame, text='Меню', command=self.init_frame_and_buttons).grid(
            row=0, column=3)

    def ask_game_end(self):
        if messagebox.askyesno('Вы уверены?', 'Точно закончить игру?', icon='warning'):
            if self.is_one_player:
                self.write_records('c')
            else:
                self.write_records(
                    'second' if self.is_first_player else 'first')
            self.init_frame_and_buttons()

        else:
            return

    def over_game(self, who=None):
        alert('Игра завершена',
              'Победил игрок' if not who else f'Победил {who}')
        if who:
            self.write_records('first' if who == 'Первый игрок' else 'second')
        else:
            self.write_records('u')
        self.init_frame_and_buttons()

    def write_records(self, param='u'):
        form = '%B %d, %Y, %H:%M:%S'
        records = open('records.txt', 'a')
        records.write(time.strftime(form) + '|')

        if param == 'c':
            records.write('Компьютер')

        if param == 'u':
            records.write('Игрок')

        if param == 'first':
            records.write('Первый игрок')

        if param == 'second':
            records.write('Второй игрок')

        records.write('\n')
        records.close()

    def show_records(self):
        try:
            records = open('records.txt', 'r')
        except:
            alert('Рекордов пока нет', 'Рекордов ещё не было')
            return

        records.seek(0)
        toplevel = Toplevel()
        frame = Frame(toplevel)
        self.window.eval(f'tk::PlaceWindow {str(toplevel)} center')
        frame.grid()

        Label(frame, text="Дата", fg='red', bg='black',
              width=25).grid(row=0, column=0)
        Label(frame, text="Победитель", fg='red', bg='black',
              width=25).grid(row=0, column=2)

        counter = 1

        if not len(records.readlines()):
            alert('Рекордов пока нет', 'Рекордов ещё не было')
            return

        records.seek(0)

        for record in records:
            date, winner = record.split('|')
            Label(frame, text=date).grid(row=counter, column=0)
            Label(frame, text=winner).grid(row=counter, column=2)
            counter += 1

        Button(frame, command=toplevel.destroy, text="Выйти").grid(
            row=counter+1, column=1)

    def show_help(self):
        toplevel = Toplevel()
        self.window.eval(f'tk::PlaceWindow {toplevel} center')

        Label(toplevel, text='Правила',
              font=self.big).grid(row=0, column=0)
        Label(toplevel, text="""Противники по очереди называют друг другу числа и сообщают о количестве
«быков» и «коров» в названном числе («бык» — цифра есть в записи
задуманного числа и стоит в той же позиции, что и в задуманном числе;
«корова» — цифра есть в записи задуманного числа, но не стоит в той же
позиции, что и в задуманном числе).
Например, если задумано число 3275 и названо число 1234, получаем в
названном числе одного «быка» и одну «корову». Очевидно, что число
отгадано в том случае, если имеем 4 «быка».""").grid(row=1, column=0)
        Button(toplevel, text="Закрыть", command=toplevel.destroy).grid(
            row=2, column=0)

    def show_credits(self):
        toplevel = Toplevel()
        self.window.eval(f'tk::PlaceWindow {toplevel} center')

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
            frame = self.frame

            Label(frame, text='Быки и коровы',
                  font=self.big).grid(row=0, column=0)

            self.window.after(8000, self.window.destroy)
        except:
            pass


def main():
    CowsAndBulls()
    mainloop()


if __name__ == '__main__':
    main()
