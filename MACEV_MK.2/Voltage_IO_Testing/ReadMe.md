# Raspberry Pi Voltage IO Testing 
[The module is capable of running a set of automated tests for voltage input/output related functions on the STM32 microcontrollers]

**References:** 
* [Documentation](https://macformulaelectric899.sharepoint.com/:w:/s/Engineering/EbZTBcyZlk1LjEFsnQlZD9YBj7xfVrFvedLbnvNeKIY_XQ?e=QD2QVy)
* [Data Brief](https://www.st.com/resource/en/data_brief/nucleo-f767zi.pdf)
* [User Manual](https://www.st.com/resource/en/user_manual/dm00244518-stm32-nucleo144-boards-mb1137-stmicroelectronics.pdf)

## Build status
Module Version: [1.2]


## Module Brief Description
[Breakdown of the module]
- **voltage_test()**: is used to run a set of voltage output tests for a specified voltage and pin value using PWM
- **push_voltage()**: is used to run voltage outputs resulting from the press of a push button by a user
- **periodic_signal()** : is used to schedule a periodic signal output every t milliseconds
- **monitor()**: is used to debounce and read input voltages for a set of specified pins
- **timing_diagram():** used to read and record voltage inputs from a pin into a timing diagram
- **debounces():** used by the monitor function to debounce the pins when needed 
- **on_press():** used by monitor() and periodic_signal() functions to stop the called function and go back user interface
 
## Detailed Description of Functions 
- **voltage_test()**:
    The function receives two arguments (voltage and pwm pin). The voltage is sent as an output to the pin that was inputted by the user. The voltage given is converted into a duty cycle percentage using the formula (Voltage Given/Max Voltage)*100 and then the duty cycle of the pwm is changed to the percentage calculated. 
    Then, the user can either change the voltage or then can go back to the main module 
    
- **push_voltage**:
    This function is very similar to the voltage_test() function. It takes three arguments, voltage, pwm pin, and push button pin. The voltage given is converted to a duty cycle and is sent to the pwm pin when the user presses the push button 
    The functions gives a option for another voltage or go back to the main module 
        
- **periodic_signal()**:
    This  function receives two arguments, pin and period. The pin is used as an output where the signal will be going. The period is the time between every signal. The function continues to run until f11 is pressed 
        
    **Important: Click esc when you want to stop this function and go back to main module**
    
    **Important: There is a variable called signal inside the function, it's basically how long the signal is going to be (pin=HIGH). As default, it's set to 1 second but can be changed directly from the variable**
        
- **monitor()**: 
    This function is designed to monitor the pins that are given by the user for signals. It receives two arguments, pins and debounce. The variable pins contains a list of pins that are being monitored for signals. Debounce is a boolean value that decides whether to debounce the pins or not 
    The function creates a log of the signals monitored and writes them to a file in an organized manner to be used later. 
    The function continues to run until the user ends it 
    
    **Important: Click esc when you want to stop this function and go back to main module**
    
    **Important: Everytime a signal is detected, a LED is flashed. The default pin for this LED is GPIO 25 but can be changed from the variable**
    
- **timing_diagram()**:
    This function is related to the monitoring function. This function takes the data that the monitoring function created and turns it into graphs for every pin used. 

- **debounces()**:
    This function is called from within the monitor function if debouncing is turned on. The function is given a set of pins and it waits for the pins to be stable for **50ms** before inputting their state. **50ms** value can be changed according to user preference. 
    
- **on_press()**
    This function is called when the user decides to end the monitor() or periodic_signal() functions. When the esc key is pressed by the user, the called function is stopped and the user is sent back to the user interface
    

## Installation
### Files Breakdown
[voltage_io.py](voltage_io.py) contains all the functions that are going to be used by the module. The detailed descriptions of these functions written above. 
[user_interface.py](user_interface.py) provides the user interface for using the module. The file allows the user to access all the functions and test them by inputting the values that are asked on the screen 

### Testing 
Open the [user_interface.py](user_interface.py) file and run it on either PI terminal or in VNC viewer. The interface provides instructions on the screen when the user runs it 

### Environment 
To test the module, you need to remotely connect your Raspberry PI to your computer. A recommended software is VNC Viewer. It allows the user to connect the PI to their computer and execute the code. Download link is given below 
[**VNC Viewer**](https://www.realvnc.com/en/connect/download/viewer/)
[**Tutorial**](https://www.youtube.com/watch?v=NWBmYnNvN3A)

### Libraries
To run the module, few additional libraries are required that might not be installed on your python. These libraries are [pynput](https://pypi.org/project/pynput/), [RPi.GPIO](https://pypi.org/project/RPi.GPIO/), [time](https://docs.python.org/3/library/time.html), [matplotlib.pyplot](https://matplotlib.org/3.3.3/contents.html)

#### Installing the Libraries 
- **Pynput**: `pip install pynput`
- **RPi.GPIO** :`pip install RPi.GPIO`
- **Matplotlib**:`python -m pip install -U matplotlib`
- **Time is already installed with python**

### Wiring 
There are two constraints for wiring. The LED pin used in the monitoring function is set to GPIO 25 but can be changed by the user. The voltage_test() and push_voltage() requires pwm pins so the user can only use pins GPIO 23 and GPIO 26 on Raspberry Pi 3B. If using Raspberry Pi 4, the pwm pins should be changed to GPIO 12 and GPIO 13 

[Pin Layout for Pi 3B](https://pi4j.com/1.2/images/j8header-3b.png)
## Authors 
- Harshpreet Chinjer
- Awurama Nyarko 
