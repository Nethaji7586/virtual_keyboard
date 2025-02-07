import cv2
import mediapipe as mp
import keyboard
import time
import winsound

# Initialize Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Allow multiple hands
mp_draw = mp.solutions.drawing_utils

# Define a simple virtual keyboard layout
keys_row_1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
keys_row_2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
keys_row_3 = ["DEL", "Z", "X", "C", "V", "B", "N", "M"]  # Added DEL key for clear

# Video feed settings
frame_width = 640
frame_height = 480

# Define key size and padding
key_width = 50  # Reduced width
key_height = 50  # Reduced height
padding = 10

# Calculate keyboard starting positions
start_x = (frame_width - (len(keys_row_1) * (key_width + padding) - padding)) // 2
start_y = frame_height - key_height - 50  # Increased bottom margin
start_y_2 = start_y + key_height + padding  # Second row of keys
start_y_3 = start_y_2 + key_height + padding  # Third row of keys

# Create a function to draw the keyboard with improved GUI
def draw_keyboard(frame):
    for idx, key in enumerate(keys_row_1):
        x = start_x + idx * (key_width + padding)
        y = start_y
        cv2.rectangle(frame, (x + 5, y + 5), (x + key_width + 5, y + key_height + 5), (50, 50, 50), -1)  # Shadow
        cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (200, 200, 255), -1)  # Key
        cv2.putText(frame, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    
    for idx, key in enumerate(keys_row_2):
        x = start_x + idx * (key_width + padding)
        y = start_y_2
        cv2.rectangle(frame, (x + 5, y + 5), (x + key_width + 5, y + key_height + 5), (50, 50, 50), -1)  # Shadow
        cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (200, 200, 255), -1)  # Key
        cv2.putText(frame, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
    
    for idx, key in enumerate(keys_row_3):
        x = start_x + idx * (key_width + padding)
        y = start_y_3
        cv2.rectangle(frame, (x + 5, y + 5), (x + key_width + 5, y + key_height + 5), (50, 50, 50), -1)  # Shadow
        cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (200, 200, 255), -1)  # Key
        cv2.putText(frame, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

    return frame

# Detect which key the fingertip is hovering over
def get_key_at_position(x, y):
    for idx, key in enumerate(keys_row_1):
        key_x = start_x + idx * (key_width + padding)
        key_y = start_y
        if key_x < x < key_x + key_width and key_y < y < key_y + key_height:
            return key
    
    for idx, key in enumerate(keys_row_2):
        key_x = start_x + idx * (key_width + padding)
        key_y = start_y_2
        if key_x < x < key_x + key_width and key_y < y < key_y + key_height:
            return key

    for idx, key in enumerate(keys_row_3):
        key_x = start_x + idx * (key_width + padding)
        key_y = start_y_3
        if key_x < x < key_x + key_width and key_y < y < key_y + key_height:
            return key
    
    return None

# Set up video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)  # Set the video feed width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)  # Set the video feed height

if not cap.isOpened():
    print("Error: Could not open video capture.")
    exit()

last_pressed = time.time()
previous_key = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror the frame
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the fingertip position (index finger tip)
            fingertip_x = int(hand_landmarks.landmark[8].x * frame.shape[1])
            fingertip_y = int(hand_landmarks.landmark[8].y * frame.shape[0])

            # Highlight the fingertip in green
            cv2.circle(frame, (fingertip_x, fingertip_y), 10, (0, 255, 0), -1)  # Green circle for fingertip

            # Highlight the key the fingertip is pointing to
            key = get_key_at_position(fingertip_x, fingertip_y)
            if key:
                # Draw a green rectangle around the hovered key
                key_index = (keys_row_1 + keys_row_2 + keys_row_3).index(key)
                if key_index < len(keys_row_1):
                    x = start_x + key_index * (key_width + padding)
                    y = start_y
                elif key_index < len(keys_row_1) + len(keys_row_2):
                    x = start_x + (key_index - len(keys_row_1)) * (key_width + padding)
                    y = start_y_2
                else:
                    x = start_x + (key_index - len(keys_row_1) - len(keys_row_2)) * (key_width + padding)
                    y = start_y_3

                cv2.rectangle(frame, (x, y), (x + key_width, y + key_height), (0, 255, 0), 2)  # Hover highlight

                if time.time() - last_pressed > 0.5:  # Only simulate key press if 0.5 seconds have passed
                    if key != previous_key:
                        if key == "DEL":
                            keyboard.press_and_release('backspace')
                        else:
                            keyboard.press_and_release(key.lower())
                        previous_key = key
                        last_pressed = time.time()

                        # Play sound on key press
                        winsound.Beep(1000, 200)  # Beep sound

    # Draw the virtual keyboard on the frame
    frame = draw_keyboard(frame)

    # Show the frame with the video feed
    cv2.imshow("Gesture-Based Virtual Keyboard", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
