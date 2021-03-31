from pynput import keyboard
import time
import RPi.GPIO as IO
import matplotlib.pyplot as plt
#imports the libraries 

break_program = False #used by the user to end a function

IO.setwarnings(False)  # ignores the warnings
IO.setmode(IO.BCM)  # uses the pins on the Raspberry PI


    
def voltage_test(voltage, pwm_pin): 
    print(
        "----------------------------------------------------------------------------"
    )
    # fake sensor outputs at various value
    IO.setup(pwm_pin, IO.OUT)  # sets the pin given as OUTPUT
    output=IO.PWM(pwm_pin,100) #100% frequency to avoid flickering 
    output.start(0) #starts the GPIO pin

    MAX_VOLTAGE = 5  # Max Voltage of PI
    duty_cycle = (voltage / MAX_VOLTAGE) * 100  # Calculation for the Duty Cycle

    if (
        duty_cycle >= 0 and duty_cycle <= 100
    ):  # checks to see if the duty cycle is valid
        output.ChangeDutyCycle(
            duty_cycle
        )  # changes the duty cycle to output the voltage required
        print("Changing the duty cycle to ", duty_cycle, "%")

    else:  # for invalid inputs
        print("Invalid Input")

    run = True 
    while run == True: #runs until the user wants to go back 
        print(
            "----------------------------------------------------------------------------"
        )
        print("1. Change the voltage\n2.Stop and Go back to the main module")
        option=-1
        while (option!=1 and option!=2):
            try: #handles the exceptions 
                option = int(input("Enter the option (1 or 2) "))  # asks the user if they want to change the voltage
            except ValueError:
                print("Please enter a valid option")

        if option == 1:
            voltage=-2.1 #place holder
            while(voltage<0 or voltage>5):
                try: #handles the exceptions 
                    voltage = float(input("Enter the new voltage ")) #gets the new voltage
                except ValueError:
                    print("Please enter a valid voltage value (between 0 and 5) ")
                    
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
    output_button=IO.PWM(pwm_pin,100) #100% frequency 
    output_button.start(0)
    
    MAX_VOLTAGE = 5  # Max Voltage of PI
    duty_cycle = (voltage / MAX_VOLTAGE) * 100  # Calculation for the Duty Cycle

    option = 1
    run = False

    while option == 1:

        if IO.input(button) == IO.HIGH:  # when button is pressed
            print("Button Pressed")
            output_button.ChangeDutyCycle(duty_cycle)  # changes the duty cycle
            print("Changing the duty cycle to ", duty_cycle, "%")
            run = True

        if run == True: #runs until the user wants to go back to the interface 
            print("1. Change the voltage\n2. Turn off and Go back to the main module")
            option=-1
            while(option!=1 and option!=2): #gets the user option
                try:
                    option = int(input("Enter the option (1 or 2) "))  # asks the user if they want to change the voltage
                except ValueError:
                    print("Please enter a valid option")

            if option == 1: #gets the new voltage 
                voltage=-1.1
                while(voltage<0 or voltage>5):
                    try: #handles exceptions 
                        voltage = float(input("Enter the new voltage "))
                    except ValueError:
                        print("Please enter a valid voltage value")
                duty_cycle = (voltage / MAX_VOLTAGE) * 100 #bew duty cycle
                run = False

            elif option == 2: #stop the function
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
    break_program=False
    print("PRESS ESC TO END THE FUNCTION")
    print("----------------------------------------------------------------------------")

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





def monitor(pins, debounce):
    print(
        "----------------------------------------------------------------------------"
    )
    file = open(
        "data.txt", "w"
    )  # opens the file for writing signal data, used for graph
    t0 = time.time()  # starts monitoring the time

    LED = 25  # LED Pin
    IO.setup(LED, IO.OUT)  # LED set as output

    length = len(pins)  # number of pins that are being monitored
    input_value = [None] * length  # stores the state of the pins

    for i in range(length):  # gets the state of the pins (HIGH/LOW)
        IO.setup(pins[i], IO.IN, pull_up_down=IO.PUD_DOWN)

        if (
            debounce == True
        ):  # if the user wants to debounce, it's done using another function
            debounces(pins[i])
        input_value[i] = IO.input(pins[i])
        file.write("%s %s %s\n" % (0, pins[i], input_value[i])) #writes the starting value to file

    # used to monitor until signal comes
    compare_value = [None] * length  # used for determining the signal
    global break_program
    break_program=False
    print("PRESS ESC TO END THE FUNCTION")
    print("----------------------------------------------------------------------------")

    with keyboard.Listener(on_press=on_press) as listener:

        while break_program == False:  # runs until a signal comes to all the pins

            time.sleep(0.1)
            IO.output(LED, 0)

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
                            LED, 1
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
                        "%s %s %s\n" % (round(t1,2), pins[i], compare_value[i])
                    )  # writes the data to the file


        listener.join()

    # compare the outputs of microcontroller
    for i in range(length):
        tfinal = time.time() - t0
        file.write("%s %s %s\n" % (round (tfinal,2), pins[i], compare_value[i]))
    file.close()
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
        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(plot_time, plot_state)  # plots the graph
        title = "Logic Analyzer for Pin: " + str(used_pins[i])  # title based on the pin
        ax.title.set_text(title)
        ax.set_xlabel("Time elsapsed", fontsize=15)
        ax.set_ylabel("Voltage", fontsize=15)
    
        plt.savefig('Pin {}'.format(used_pins[i]))
    plt.show()  # shows the graph on the screen


    # captures the diagnostic data
    file.close()
    return

def on_press(key):  # function to detect key press
    print(
        "----------------------------------------------------------------------------"
    )
    global break_program
    print(key)
    if key == keyboard.Key.esc:  # checks if the escape key is pressed
        print("esc pressed")
        break_program = True  # stops the program
        return False

def debounces(pin):  # Used for debouncing the pin
    # gets the state of the pin and waits for it be to be stable for 50ms

    cur_value = IO.input(pin)
    active = 0
    while active < 50: #change this value to adjust debounce time in milliseconds
        if IO.input(pin) == cur_value:
            active += 1
        else:
            active = 0
            cur_value = IO.input(pin)
            time.sleep(0.1)
        time.sleep(0.001)
    # have to be stable for 50ms
    return


