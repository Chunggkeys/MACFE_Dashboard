# Raspberry Pi Voltage IO Testing 
[The module is capable of running a set of automated tests for voltage input/output related functions on the STM32 microcontrollers]

**References:** 
* [Documentation](https://macformulaelectric899.sharepoint.com/:w:/s/Engineering/EbZTBcyZlk1LjEFsnQlZD9YBj7xfVrFvedLbnvNeKIY_XQ?e=QD2QVy)
* [Data Brief](https://www.st.com/resource/en/data_brief/nucleo-f767zi.pdf)
* [User Manual](https://www.st.com/resource/en/user_manual/dm00244518-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf)

## Build status
Module Version: [1.0]

[Still needs more work on exception handling and efficiency]

## Module Brief Description
[Breakdown of the module]
- **voltage_test()**: is used to run a set of voltage output tests for a specified voltage and pin value using PWM
- **push_voltage()**: is used to run voltage outputs resulting from the press of a push button by a user
- **periodic_signal()** : is used to schedule a periodic signal output every t milliseconds
- **monitor()**: is used to debounce and read input voltages for a set of specified pins
- **timing_diagram():** used to read and record voltage inputs from a pin into a timing diagram

## Detailed Description of Functions 
- **voltage_test()**:
    The function recieves two arguments (voltage and pwm pin). The voltage is sent as an output to the pin that was inputed by the user. The voltage given is converted into a duty cycle percentage using the formula $$\left(\frac {voltage\:given}{MAX\:Voltage}\right)\times100$$ and then the duty cycle of the pwm is changed to the percentage calculated. 
    Then, the user can either change the voltage or then can go back to the main module 
    
- **push_voltage**:
    This function is very similar to the voltage_test() function. It takes three arguments, voltage, pwm pin, and push button pin. The voltage given is converted to a duty cycle and is sent to the pwm pin when the user presses the push button 
    The functions gives a option for another voltage or go back to the main module 
        
- **periodic_signal()**:
    This  function recieves two arguments, pin and period. The pin is used an output where the signal will be going. The period is the time between every signal. The function continues to run until f11 is pressed 
        
    **Important: Click f11 when you want to stop this function and go back to main module**
    
    **Important: There is a variable called signal inside the function, it's basicially how long the signal is going to be (pin=HIGH). As default, it's set to 1 second but can be changed directly from the variable**
        
- **monitor()**: 
    This function is designed to monitor the pins that are given by the user for signals. It recieves two argument, pins and debounce. The variable pins contains a list of pins that are being monitored for signals. Debounce is a boolean value that decides whether to debounce the pins or not 
    The function creates a log of the signals monitored and writes them to a file in an organized manner to be used later. 
    The function continues to run until the user ends it 
    
    **Important: Click f11 when you want to stop this function and go back to main module**
    
    **Important: Everytime a signal is detected, a LED is flashed. The default pin for this LED is GPIO 25 but can be changed from the variable**
    
- **timing_diagram()**:
    This function is related to the monitoring function. This function takes the data that the monitroing function created and turns it into graphs for every pin used. 
    

## Installation
### Libraries
To run the module, few additional libraries are required that might not be installed on your python. These libraries are [pynput](https://pypi.org/project/pynput/), [RPi.GPIO](https://pypi.org/project/RPi.GPIO/), [time](https://docs.python.org/3/library/time.html), [matplotlib.pyplot](https://matplotlib.org/3.3.3/contents.html)

#### Installing the Libraries 
- **Pynput**: `pip install pynput`
- **RPi.GPIO** :`pip install RPi.GPIO`
- **Matplotlib**:`python -m pip install -U matplotlib`
- **Time is already installed with python**

### Wiring 
There are two constraints for wiring. The LED pin used in monitoring function is set to GPIO 25 but can be changed by the user. The voltage_test() and push_voltage() requires pwm pins so the user can only use GPIO 23, GPIO 26, or GPIO 1

[Pin Layout for Pi 3B](https://pi4j.com/1.2/images/j8header-3b.png)
## Authors 
- Harshpreet Chinjer
- Awurama Nyarko 