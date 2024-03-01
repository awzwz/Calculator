import tkinter as tk
import math
import pygame
from pygame import mixer

LARGE_FONT_STYLE = ("Arial", 50, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
SPECIAL_FUNC_COLOR = "#ACC0F2"

mixer.init()

# When we creating buttons or labels see def functions to create, we creating it with tk.Label or tk.Button
# And setting the configurations to label or button and so an
# (Characteristics like background, font, maybe size, padx, color like that)

class Calculator:
    def __init__(self):
        pygame.init()

        self.window = tk.Tk()
        self.window.geometry("500x700")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        # Sounds
        # Getting the path to sound and set the click_sound, now in self.click_sound we contain the sound
        self.click_sound = pygame.mixer.Sound("C:\\Users\\Acer\\Downloads\\Calculator-master\\sounds\\click_sound.wav")

        self.total_expression = "" # Of course we need to have a empty expression at first, total сверху
        self.current_expression = "" # Of course we need to have a empty expression at first, current снизу
        self.display_frame = self.create_display_frame() # ?

        self.total_label, self.label = self.create_display_labels()

        self.digits = { # Object to positioning the digits
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"} # Also object ot contain operations
        # Объект работает по принципу ключ - значение in now we have key "*" and his value "\u00D7"
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 6):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    # def to create special buttons and it works like ...
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_sin_button()
        self.create_cos_button()
        self.create_tan_button()
        self.create_exp_button()
        self.create_power_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg="LIGHT BLUE",
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE) # font - шрифт текста
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    # Just adding value to expression Value like (1,2,3,4,5, ... or +, -, /, * and so on)
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    # works in the same reason like add_to_expresion
    # we have a "operator"
    def append_operator(self, operator):
        self.current_expression += operator # And we add the operator to current expression
        self.total_expression += self.current_expression # Then also in total expression
        self.current_expression = "" # And of course we need to do empty current expression
        self.update_total_label() # and we MUST update labels
        self.update_label()

    # Watch indus in video, but this def is for creating operato buttons
    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    # In logical way we need to do empty expressions in current and total
    def clear(self):
        self.click_sound.play()
        self.current_expression = ""
        self.total_expression = ""
        self.update_label() # And of course we must update label
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.click_sound.play()
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=5, sticky=tk.NSEW)



    # def tan(self):
    #     try:
    #         result = math.tan(eval(self.current_expression)) # То есть посчитай мне текущий expression and give me result
    #         self.current_expression = str(result) # And we convert the result to string with function str()
    #     except Exception as e: # If user added something wrong we prin Error
    #         self.current_expression = "Error"
    #     self.update_label() # If try sucessfully worked, we must update the label
    def tan(self):
        try:
            radians = math.radians(eval(self.current_expression))  # Convert degrees to radians
            result = math.sin(radians) / math.cos(radians)
            self.current_expression = str(result)
        except Exception as e:
            print(e)
            self.current_expression = "Error"
        self.update_label()
    def create_tan_button(self):
        button = tk.Button(self.buttons_frame, text="tan", bg=SPECIAL_FUNC_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.tan)
        button.grid(row=3, column=5, sticky=tk.NSEW)

    def exp(self):
        self.current_expression = str(math.exp(float(self.current_expression)))  # Using math.exp for exponentiation
        self.update_label()

    def create_exp_button(self):
        button = tk.Button(self.buttons_frame, text="exp", bg=SPECIAL_FUNC_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.exp)
        button.grid(row=4, column=5, sticky=tk.NSEW)

    def power(self):
        self.current_expression += "^"
        self.update_label()
        base, exponent = self.total_expression.split("^")
        # print(base, exponent)
        # self.current_expression = str(pow(float(base), float(exponent)))
        self.total_expression = f"pow({float(base)}, {float(exponent)})"
        self.update_label()


    def create_power_button(self):
        button = tk.Button(self.buttons_frame, text="^", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=self.power)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    #

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            if "^" in self.total_expression:
                self.power()
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def sin(self):
        try:
            radians = math.radians(eval(self.current_expression))  # Convert degrees to radians
            result = math.sin(radians)
            self.current_expression = str(result)
        except Exception as e:
            print(e)
            self.current_expression = "Error"
        self.update_label()

    def create_sin_button(self):
        button = tk.Button(self.buttons_frame, text="sin", bg=SPECIAL_FUNC_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sin)
        button.grid(row=1, column=5, sticky=tk.NSEW)

    def cos(self):
        try:
            radians = math.radians(eval(str(self.current_expression)))  # Convert degrees to radians
            result = math.cos(radians)
            self.current_expression = str(result)
        except Exception as e:
            print(e)
            self.current_expression = "Error"
        self.update_label()

    def create_cos_button(self):
        button = tk.Button(self.buttons_frame, text="cos", bg=SPECIAL_FUNC_COLOR, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sin)
        button.grid(row=2, column=5, sticky=tk.NSEW)
    # def evaluate(self):
    #     try:
    #         self.current_expression = str(eval(self.current_expression))
    #     except Exception as e:
    #         self.current_expression = "Error"
    #     self.update_label()

    # def create_equals_button(self):
    #     button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
    #                        borderwidth=0, command=self.evaluate)
    #     button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression) # If we changed something in expression, we must to update the label also

    def update_label(self):
        # If we changed something in expression, we must to update the label also
        self.label.config(text=self.current_expression[:11])

    def run(self):
        self.window.mainloop() # Runnig main loop while we don't close the window


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
