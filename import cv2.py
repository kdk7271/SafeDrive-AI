import cv2

def find_available_cameras(max_index=5):
    available_cameras = []
    for i in range(max_index):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras

cameras = find_available_cameras()
print("사용 가능한 카메라 인덱스:", cameras)