import cv2, sys

cap = cv2.VideoCapture(0)
cv2.namedWindow('Frame', cv2.WINDOW_NORMAL)

# Our ROI, defined by two points
p1, p2 = None, None
state = 0

# Called every time a mouse event happen
def on_mouse(event, x, y, flags, userdata):
    global state, p1, p2
    global state, p3, p4
    # Left click
    if event == cv2.EVENT_LBUTTONUP:
        # Select first point
        if state == 0:
            p1 = (x-25,y+25)
            state += 1
            p2 = (x+25,y-25)

        # Select second point
        elif state == 1:
            p3 = (x-25,y+25)
            state += 1
            p4 = (x+25,y-25)
    # Right click (erase current ROI)
    if event == cv2.EVENT_RBUTTONUP:
        p1, p2 = None, None
        p3, p4 = None, None
        state = 0

# Register the mouse callback
cv2.setMouseCallback('Frame', on_mouse)

while cap.isOpened():
    val, frame = cap.read()
    
    # If a ROI is selected, draw it
    if state == 1:
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 10)
    elif state == 2:
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 10)
        cv2.rectangle(frame, p3, p4, (255, 0, 0), 10)
    # Show image
    
    cv2.imshow('Frame', frame)
    
    # Let OpenCV manage window events
    key = cv2.waitKey(50)
    # If ESCAPE key pressed, stop
    if key == 27:
        cap.release()