from ultralytics import YOLO
import cv2, time, requests
import os
from dotenv import load_dotenv

load_dotenv()

COOLDOWN_SECONDS = 15
LAST_TRIGGER_TIME = 0
TEMPO_DE_ESPERA_NA_PORTA = 10
RTSP_URL = os.getenv("RTSP_URL")
VOICE_MONKEY_TRIGGER_URL = os.getenv("VOICE_MONKEY_TRIGGER_URL")
entrada_area = 0.0
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"

def trigger_alexa():
    global LAST_TRIGGER_TIME
    now = time.time()
    if now - LAST_TRIGGER_TIME > COOLDOWN_SECONDS:
        try:
            requests.get(VOICE_MONKEY_TRIGGER_URL, timeout=3)
            print("🔔 Alexa notificada!")
            LAST_TRIGGER_TIME = now
        except Exception as e:
            print(f"Erro: {e}")

def inside_area(x, y, area):
    (x1, y1, x2, y2) = area
    return x1 < x < x2 and y1 < y < y2

def main():
    print("Iniciando monitoramento de área...")


    # Área de interesse
    dax1, day1, dax2, day2 = 134, 100, 550, 360
    
    global entrada_area
    global TEMPO_DE_ESPERA_NA_PORTA

    cap = cv2.VideoCapture(RTSP_URL)
    model = YOLO("yolov8n.pt")

    frame_skip = 2

    frame_count = 0
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("⚠️ Sinal da câmera caiu. Tentando reconectar...")
            cap.release()
            time.sleep(2)
            cap = cv2.VideoCapture(RTSP_URL)
            continue
            
        frame_count += 1
        frame = cv2.resize(frame, (640, 480))
        
        # 1. Desenha a área de monitoramento na tela em TODOS os frames
        cv2.rectangle(frame, (dax1, day1), (dax2, day2), (255, 0, 0), 2)

        # 2. Só roda o YOLO se for o frame correto (frame_skip)
        if frame_count % frame_skip == 0:
            pessoa_detectada_na_area_neste_frame = False
            
            for r in model(frame, imgsz=480, conf=0.5, stream=True, verbose=False):
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = model.names[cls]
                    if name == "person":
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                        cx, cy = (x1 + x2)//2, (y1 + y2)//2

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
                        if inside_area(cx, cy, (dax1, day1, dax2, day2)):
                            pessoa_detectada_na_area_neste_frame = True
                            print("Pessoa detectada dentro da área!")

                            if entrada_area == 0.0:
                                entrada_area = time.time()

                            now = time.time()
                            print(f"Tempo na área: {now - entrada_area:.2f} segundos")
                            
                            if now - entrada_area > TEMPO_DE_ESPERA_NA_PORTA:
                                trigger_alexa()
                                entrada_area = 0.0
                
                if not pessoa_detectada_na_area_neste_frame and entrada_area != 0.0:
                    print("Pessoa saiu da área. Zerando cronômetro.")
                    entrada_area = 0.0
                    
        # 3. Exibe a janela e roda o waitKey em TODOS os frames
        cv2.imshow("Monitoramento do Portao", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
