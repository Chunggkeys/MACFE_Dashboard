from pynput import keyboard
import time
import RPi.GPIO as IO
import matplotlib.pyplot as plt

break_program = False
output = None
output_button = None
IO.setwarnings(False)  # ignores the warnings
IO.setmode(IO.BCM)  # uses the pins on the Raspberry PI


def voltage_test(voltage, pwm_pin):
    print(
        "----------------------------------------------------------------------------"
    )
    # fake sensor outputs at various values
    IO.setup(pwm_pin, IO.OUT)  # sets the pin given as OUTPUT

    MAX_VOLTAGE = 5  # Max Voltage of PI
    duty_cycle = (voltage / MAX_VOLTAGE) * 100  # Calculation for the Duty Cycle

    if (
        duty_cycle >= 0 and duty_cycle <= 100
    ):  # checks to see if the duty cycle is valid
        global output
        output.ChangeDutyCycle(
            duty_cycle
        )  # changes the duty cycle to output the voltage required
        print("Changing the duty cycle to ", duty_cycle, "%")

    else:  # for invalid inputs
        print("Invalid Input")

    run = True
    while run == True:
        print(
            "----------------------------------------------------------------------------"
        )
        print("1. Change the voltage\n2.Turn off and Go back to the main module")
        option = int(
            input("Enter the option (1 or 2) ")
        )  # asks the user if they want to change the voltage

        if option == 1:
            voltage = float(input("Enter the new voltage "))
            duty_cycle = (voltage / MAX_VOLTAGE) * 100  # calculates the new duty cycle
            output.ChangeDutyCycle(
                duty_cycle
            )  # changes the duty cycle to output the voltage required
            print("Changing the duty cycle to ", duty_cycle, "%")
        elif option == 2:
            run = False
            output.stop()
        else:
            print("Invalid Option")

    return


def push_voltage(voltage, pwm_pin, button):
    print(
        "----------------------------------------------------------------------------"
    )
    IO.setup(pwm_pin, IO.OUT)  # sets the pin given as OUTPUT
    IO.setup(button, IO.IN, pull_up_down=IO.PUD_DOWN)  # sets the push button as INPUT

    MAX_VOLTAGE = 5  # Max Voltage of PI
    duty_cycle = (voltage / MAX_VOLTAGE) * 100  # Calculation for the Duty Cycle

    global output_button

    option = 1
    run = False

    while option == 1:

        if IO.input(button) == IO.HIGH:  # when button is pressed
            print("Button Pressed")
            output_button.ChangeDutyCycle(duty_cycle)  # changes the duty cycle
            print("Changing the duty cycle to ", duty_cycle, "%")
            run = True

        if run == True:
            print("1. Change the voltage\n2. Turn off and Go back to the main module")
            option = int(
                input("Enter the option (1 or 2) ")
            )  # asks the user if they want to change the voltage

            if option == 1:
                voltage = float(input("Enter the new voltage "))
                duty_cycle = (voltage / MAX_VOLTAGE) * 100
                run = False

            elif option == 2:
                output_button.stop()
                print("Returning to the main module")

    # fake input signals for the microcontroller
    return


def periodic_signal(pin, period):
    print(
        "----------------------------------------------------------------------------"
    )
    IO.setup(pin, IO.OUT)  # sets the pin given as OUTPUT

    signal = 1  # 1 second signal

    run = True  # used to run the program until key is pressed

    global break_program  # used to stop the program
    print("PRESS F11 WHEN YOU WANT TO END THIS FUNCTION")

    with keyboard.Listener(on_press=on_press) as listener:  # works until f11 is pressed
        while break_program == False:

            print("Sending a signal for 1 second")
            IO.output(pin, 1)  # sets the pin HIGH
            time.sleep(signal)
            IO.output(pin, 0)  # sets the pin LOW
            # sends the periodic signal for 1second

            time.sleep(period)
            # waits for the given period

        listener.join()

    # fakes input signals for the microcontroller
    IO.output(pin, 0)
    return


def on_press(key):  # function to detect key press
    print(
        "----------------------------------------------------------------------------"
    )
    global break_program
    print(key)
    if key == keyboard.Key.f11:  # checks if the Delete key is pressed
        print("f11 pressed")
        break_program = True  # stops the program
        return False


def monitor(pins, debounce):
    print(
        "----------------------------------------------------------------------------"
    )
    file = open(
        "data.txt", "w"
    )  # opens the file for writing signal data, used for graph
    t0 = time.time()  # starts monitoring the time

    led_pin = 25  # LED Pin
    IO.setup(led_pin, IO.OUT)  # LED set as output

    length = len(pins)  # number of pins that are being monitored
    input_value = [None] * length  # stores the state of the pins

    for i in range(length):  # gets the state of the pins (HIGH/LOW)
        IO.setup(pins[i], IO.IN, pull_up_down=IO.PUD_DOWN)

        if (
            debounce == True
        ):  # if the user wants to debounce, it's done using another function
            debounces(pins[i])
        input_value[i] = IO.input(pins[i])
        file.write("%s %s %s\n" % (0, pins[i], input_value[i]))

    # used to monitor until signal comes
    compare_value = [None] * length  # used for determining the signal
    global break_program
    print("Press F11 WHEN YOU WANT TO END THIS FUNCTION")

    with keyboard.Listener(on_press=on_press) as listener:

        while break_program == False:  # runs until a signal comes to all the pins

            time.sleep(0.1)
            IO.output(led_pin, 0)

            for i in range(length):  # gets the current state of the pins
                if debounce == True:  # debounce
                    debounces(pins[i])
                compare_value[i] = IO.input(pins[i])
                if (
                    input_value[i] != compare_value[i]
                ):  # detects the signal by comparing the current state to previous state
                    t1 = (
                        time.time() - t0
                    )  # gets the time at when the signal was detected

                    if compare_value[i] == IO.HIGH:
                        print(
                            "Signal Detected for pin",
                            pins[i],
                            " at ",
                            round(t1, 2),
                            " seconds",
                        )
                        IO.output(
                            led_pin, 1
                        )  # lights up the LED to show that a signal came
                    else:
                        print(
                            "Signal Lost for pin",
                            pins[i],
                            " at ",
                            round(t1, 2),
                            " seconds",
                        )

                    input_value[i] = compare_value[
                        i
                    ]  # the latest state of the pin is stored in input_value

                    file.write(
                        "%s %s %s\n" % (t1, pins[i], compare_value[i])
                    )  # writes the data to the file

                    # implement a led light up

        listener.join()

    # compare the outputs of microcontroller
    for i in range(length):
        tfinal = time.time() - t0
        file.write("%s %s %s\n" % (tfinal, pins[i], compare_value[i]))
    file.close()
    return


def debounces(pin):  # Used for debouncing the pin
    # gets the state of the pin and waits for it be to be stable for 50ms

    cur_value = IO.input(pin)
    active = 0
    while active < 50:
        if IO.input(pin) == cur_value:
            active += 1
        else:
            active = 0
            cur_value = IO.input(pin)
            time.sleep(0.1)
        time.sleep(0.001)
    # have to be stable for 50ms
    return


def timing_diagram(used_pins):
    file = open("data.txt", "r")
    timer = []  # stores the time
    pins = []  # stores the pin numbers
    state = []  # stores the state of the pin

    data = file.readlines()  # reads the document

    for i in data:
        t, p, s = i.split(" ")
        s = s.strip("\n")
        timer.append(float(t))
        pins.append(int(p))
        state.append(int(s) * 5)
    # used to read the data into 3 different variables

    pins_length = len(used_pins)  # number of pins used
    timer_length = len(timer)  # amount of signals detected

    for i in range(pins_length):
        plot_time = []  # stores the time plotting points
        plot_state = []  # stores the state for plotting
        for j in range(timer_length):

            if pins[j] == used_pins[i]:
                plot_time.append(timer[j])
                plot_state.append(state[j])
                # sorts the data according to the pin number

                """
                the block below is used to plot extra data points on the graph
                to avoid diagonal lines on the graph. It gives the graph a more
                logic analyzer look and shows the straight line duty cycles 
                """
                check = True
                temp = j + 1
                while check == True:

                    if temp < timer_length:
                        if pins[temp] == used_pins[i]:
                            plot_time.append(timer[temp])
                            plot_state.append(state[j])
                            check = False
                        else:
                            temp += 1
                    else:
                        check = False

        plt.plot(plot_time, plot_state)  # plots the graph
        title = "Logic Analyzer for Pin: " + str(used_pins[i])  # title based on the pin
        plt.title(title)
        plt.xlabel("Time elapsed")
        plt.ylabel("Voltage")
        plt.show()  # shows the graph on the screen

    # captures the diagnostic data
    file.close()
    return


def main():
    run = True  # runs the while loop

    global break_program  # used for stop periodic and monitoring functions
    global output_button  # used to change voltage for push button function
    global output  # used to change voltage for the test voltage function

    while run == True:  # runs until user exits

        print(
            "----------------------------------------------------------------------------"
        )  # just for organizing
        print(
            "1. Voltage Test\n2. Push button\n3. Periodic Signal\n4. Monitor Pins\n5. Timing Diagrams\n6. End Program"
        )  # user options
        print(
            "----------------------------------------------------------------------------"
        )
        option = int(input("Enter the option number "))  # gets the user inputs

        while option > 6 or option < 1:
            print(
                "----------------------------------------------------------------------------"
            )
            option = int(
                input("Invalid option: Enter the option number again")
            )  # handles invalid option

        if option == 1:  # runs the voltage test function
            print(
                "----------------------------------------------------------------------------"
            )

            voltage = float(
                input("Enter the voltage that you want to output ")
            )  # gets voltage
            pin = int(input("Enter the pwm pin you want to use "))  # gets the pwm pin

            while (voltage < 0 or voltage > 5) or (
                pin != 23 and pin != 26 and pin != 1
            ):  # handles exceptions
                print(
                    "----------------------------------------------------------------------------"
                )
                print("Invalid Input, Please Enter the Information Again")
                voltage = float(input("Enter the voltage that you want to output "))
                pin = int(input("Enter the pwm pin you want to use "))

            IO.setup(pin, IO.OUT)  # sets the pin as output
            output = IO.PWM(
                pin, 100
            )  # sets the PWM to 100 frequency to avoid flickering
            output.start(0)  # starts the pwm pin

            voltage_test(voltage, pin)  # calls the function

        elif option == 2:  # runs push_voltage function
            print(
                "----------------------------------------------------------------------------"
            )

            voltage_button = float(
                input("Enter the voltage that you want to output ")
            )  # gets the voltage
            pin_button = int(
                input("Enter the pwm pin you want to use ")
            )  # gets the pwm pin
            push_button = int(
                input("Enter the pin for push button ")
            )  # gets the pin for push button

            while (
                (voltage_button < 0 or voltage_button > 5)
                or (pin_button != 23 and pin_button != 26 and pin_button != 1)
                or (push_button < 0)
            ):  # handles exceptions
                print(
                    "----------------------------------------------------------------------------"
                )
                print("Invalid Input, Enter the Information Again")
                voltage_button = float(
                    input("Enter the voltage that you want to output ")
                )
                pin_button = int(input("Enter the pwm pin you want to use "))
                push_button = int(input("Enter the pin for push button "))

            IO.setup(pin_button, IO.OUT)  # sets the pwm pin as output
            output_button = IO.PWM(pin_button, 100)  # sets the frequency to 100
            output_button.start(0)  # starts the pwm channel

            push_voltage(
                voltage_button, pin_button, push_button
            )  # calls the push_voltage function

        elif option == 3:  # runs the periodic_signal function
            print(
                "----------------------------------------------------------------------------"
            )
            pin_period = int(
                input("Enter the pin for periodic signals ")
            )  # gets the pin for the signal
            period = float(
                input("Enter the period between signals in milliseconds ")
            )  # gets the period for signal

            while (pin_period < 0) or (period < 0):  # handles the exceptions
                print(
                    "----------------------------------------------------------------------------"
                )
                print("Invalid Input, Enter the information again ")
                pin_period = int(input("Enter the pin for periodic signals "))
                period = float(
                    input("Enter the period between signals in milliseconds ")
                )

            period = period / 1000  # converts the milliseconds to seconds
            break_program = False  # starts the loop that is stopped by pressing f11
            periodic_signal(pin_period, period)  # calls the periodic signal function

        elif option == 4:  # runs the monitoring pin function
            print(
                "----------------------------------------------------------------------------"
            )
            length = int(
                input("Enter the number of pins you want to monitor ")
            )  # gets the amount of pins

            while length < 0:  # handles exceptions
                print(
                    "----------------------------------------------------------------------------"
                )
                print("No negative length allowed ")
                length = int(
                    input("Enter the number of pins you want to monitor ")
                )  # gets the amount of pins

            pins = [None] * length  #

            for i in range(length):  # gets the number for all the pins
                pins[i] = int(input("Enter the pin number: "))

            debouncing = int(
                input("Do you want to debounce the pins (Enter 1 for YES, 2 for NO) ")
            )  # asks for debounce

            if debouncing == 1:
                debounce = True  # sends it as an argument

            break_program = False  # used to stop the loop when key is pressed

            monitor(pins, debouncing)  # calls the monitoring function
            executed = (
                +1
            )  # used to avoid the error of calling the fifth function before calling the fourth

        elif option == 5:  # calls the diagram function
            print(
                "----------------------------------------------------------------------------"
            )
            if executed > 0:
                timing_diagram(pins)  # calls the diagram function
            else:
                print("Run the monitoring function before drawing the graph ")

        elif option == 6:  # ends the program
            print(
                "----------------------------------------------------------------------------"
            )
            print("Ending program...")
            run = False  # breaks the main module loop


main()
