# Dashboard

Code for the dashboard.

This short tutorial is assuming the user has a python3 environment configured

testGUI.sh is used to test the GUI only. It changes GUI based on random values
Execute script file by navigating to this directory and using ./testGUI.sh

If you would like to test values of your own, you can input them yourself using the following steps:
1. navigate to this directory and run "python3 view.py" terminal and hit enter
2. Open new terminal instance and start python interpreter by using "python3" in terminal and hit enter
3. In the interpreter, type "import guiModel as gm", then hit enter
4. Based on the setters in guiModel.py (As commented in the code), you can type, for example, "gm.setBatteryLevel(30)"
5. Watch to see how GUI behaves. You can use other setters to see behavior of other elements in the GUI

The config file in this repo is to be placed in /boot directory of the Pi. 