# Gesture-Based Virtual Keyboard📱

A gesture-based virtual keyboard using hand tracking with MediaPipe and OpenCV. This application allows users to type on a virtual keyboard by simply pointing at the keys with their fingers, simulating key presses on the system. It uses a webcam to detect hand landmarks and triggers key presses based on finger positioning.

## Features

- **Hand Gesture Recognition**: Uses MediaPipe's hand tracking model to detect hand landmarks and recognize gestures.
- **Virtual Keyboard**: Displays a virtual keyboard on the screen with interactive keys that can be "pressed" by pointing at them with the index finger.
- **Key Simulation**: The detected keys are simulated using the `keyboard` module to type text or press special keys (e.g., backspace).
- **Sound Feedback**: A beep sound plays whenever a key is pressed to provide auditory feedback.

## Requirements

To run the virtual keyboard, ensure you have the following libraries installed:

- Python 3.x
- OpenCV
- MediaPipe
- `keyboard` (for simulating key presses)
- `winsound` (for playing sound on key presses)

You can install the required libraries using the following:

```bash
pip install opencv-python mediapipe keyboard
```
Setup and Usage
Clone the Repository: First, clone this repository or download the code.
```
git clone https://github.com/your-username/gesture-based-virtual-keyboard.git
```
Install Dependencies: Install the required Python libraries.
```
pip install opencv-python mediapipe keyboard
```
