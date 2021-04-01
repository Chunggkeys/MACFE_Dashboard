import RPi.GPIO as IO
import voltage_io
IO.setwarnings(False)
IO.setmode(IO.BCM)
executed = 0


def main():
    run = True  # runs the while loop

    global break_program  # used for stop periodic and monitoring functions
    global output_button  # used to change voltage for push button function
    global output  # used to change voltage for the test voltage function
    global executed

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

        option = 9
        while option > 6 or option < 1: #exception handling
            try:
                option = int(
                    input("Enter the option number ")
                )  # gets the option number
            except ValueError:
                print("Please enter a valid number")

        if option == 1:  # runs the voltage test function
            print(
                "----------------------------------------------------------------------------"
            )
            voltage = -1.5
            while voltage < 0 or voltage > 5:
                try:
                    voltage = float(input("Enter the output voltage "))  # gets voltage
                except ValueError:
                    print("Please enter a valid voltage value")

            pin = -1
            while pin != 23 and pin != 26:
                try:
                    pin = int(
                        input("Enter the pwn pin (23 or 26) ") #PWM pins of PI 3B
                        #Change the pins to 12 and 13 if testing on PI 4
                    )  # gets the pwm pin
                except ValueError:
                    print("Please enter a valid pwm pin number")

            from voltage_io import voltage_test  # calls the function

            voltage_test(voltage, pin)

        elif option == 2:  # runs push_voltage function
            print(
                "----------------------------------------------------------------------------"
            )

            voltage_button = -1.5
            pin_button = -1
            push_button = -1

            while voltage_button < 0 or voltage_button > 5:
                try:
                    voltage_button = float(input("Enter the output voltage "))
                except ValueError:
                    print("Please enter a valid voltage value")

            while pin_button != 23 and pin_button != 26:  # pwm pins on PI 3B
                try:
                    pin_button = int(input("Enter the pwm pin (23 or 26) "))
                except ValueError:
                    print("Please enter a valid pwm pin number ")

            while push_button < 2 or push_button > 27:
                try:
                    push_button = int(
                        input("Enter the push button pin (GPIO pins 2-27) ")
                    )
                except ValueError:
                    print("Please enter a valid pin number")

            from voltage_io import push_voltage

            push_voltage(
                voltage_button, pin_button, push_button
            )  # calls the push_voltage function

        elif option == 3:  # runs the periodic_signal function
            print(
                "----------------------------------------------------------------------------"
            )
            pin_period = -1
            period = -1

            while pin_period < 2 or pin_period > 27:
                try:
                    pin_period = int(
                        input("Enter the pin for periodic signals ")
                    )  # gets the pin for the signal
                except ValueError:
                    print("Please enter a valid pin number")

            while period < 0:
                try:
                    period = float(
                        input("Enter the period between signals in milliseconds ")
                    )  # gets the period for signal
                except ValueError:
                    print("Please enter a valid period")

            period = period / 1000  # converts the milliseconds to seconds
            from voltage_io import periodic_signal

            periodic_signal(pin_period, period)  # calls the periodic signal function

        elif option == 4:  # runs the monitoring pin function
            print(
                "----------------------------------------------------------------------------"
            )
            length = -1

            while length < 1:  # minimum 1 pin
                try:
                    length = int(
                        input("Enter the number of pins you want to monitor ")
                    )  # gets the amount of pins
                except ValueError:
                    print("Please enter a valid length")

            pins = [-1] * length  #
            count = 0
            debounce = False

            while count < length:
                try:
                    pins[count] = int(
                        input("Enter the pin number {} ".format(count + 1))
                    )
                    if (
                        pins[count] >= 2 and pins[count] <= 27 and pins[count] != 25
                    ):  # 25 in the LED pin, if changed here, change in functions file as well
                        count += 1
                except ValueError:
                    print("Please enter a valid pin number")

            debouncing = 3
            while debouncing != 1 and debouncing != 2:
                try:
                    debouncing = int(
                        input(
                            "Do you want to debounce the pins (Enter 1 for YES, 2 for NO) "
                        )
                    )  # asks for debounce
                except ValueError:
                    print("Please enter a valid option")

            if debouncing == 1:
                debounce = True  # sends it as an argument

            from voltage_io import monitor

            monitor(pins, debounce)  # calls the monitoring function

            executed += 1  # used to avoid the error of calling the fifth function before calling the fourth

        elif option == 5:  # calls the diagram function
            print(
                "----------------------------------------------------------------------------"
            )
            from voltage_io import timing_diagram

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
