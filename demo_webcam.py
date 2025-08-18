import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Abrir webcam con DirectShow para que sea rápido en Windows
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("No se pudo abrir la cámara 0")
#else:
#    print("Cámara abierta con éxito")
#cap.release()
    exit()

with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir a RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Procesar con MediaPipe
        results = pose.process(image)

        # Dibujar resultados sobre la imagen original
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('MediaPipe Pose Demo', image)

        if cv2.waitKey(5) & 0xFF == 27:  # Esc para salir
            break

cap.release()
cv2.destroyAllWindows()
