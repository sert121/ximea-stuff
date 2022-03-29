import os
import cv2, sys

cap = cv2.VideoCapture(0)
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)

config = {"FRAME_HALF_WIDTH": 25, "FRAME_WEIGHT": 2}

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
            p1 = (x - config["FRAME_HALF_WIDTH"], y + config["FRAME_HALF_WIDTH"])
            state += 1
            p2 = (x + config["FRAME_HALF_WIDTH"], y - config["FRAME_HALF_WIDTH"])

        # Select second point
        elif state == 1:
            p3 = (x - config["FRAME_HALF_WIDTH"], y + config["FRAME_HALF_WIDTH"])
            state += 1
            p4 = (x + config["FRAME_HALF_WIDTH"], y - config["FRAME_HALF_WIDTH"])
    # Right click (erase current ROI)
    if event == cv2.EVENT_RBUTTONUP:
        p1, p2 = None, None
        p3, p4 = None, None
        state = 0


# Register the mouse callback
cv2.setMouseCallback("Frame", on_mouse)

while cap.isOpened():
    val, frame = cap.read()

    # If a ROI is selected, draw it
    if state == 1:
        cv2.rectangle(frame, p1, p2, (255, 0, 0), config["FRAME_WEIGHT"])
    elif state == 2:
        cv2.rectangle(frame, p1, p2, (255, 0, 0), config["FRAME_WEIGHT"])
        cv2.rectangle(frame, p3, p4, (255, 0, 0), config["FRAME_WEIGHT"])

        # save roi frame
        roi_img_1 = frame[p2[1] : p1[1], p1[0] : p2[0]].copy()
        roi_img_2 = frame[p4[1] : p3[1], p3[0] : p4[0]].copy()
        # cv2.imshow("roi", roi_img)

    # Show image
    cv2.imshow("Frame", frame)

    # last 8 bits of keypress binary
    key = cv2.waitKey(50) & 0xFF

    # `s` or `S` to save ROIs
    if key == ord("s") or key == ord("S"):
        cv2.imwrite(f"{os.curdir}/saved_images/roi_1.png", roi_img_1)
        cv2.imwrite(f"{os.curdir}/saved_images/roi_2.png", roi_img_2)

    # ESC key to exit
    if key == 27:
        cap.release()
