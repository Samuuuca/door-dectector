import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do sistema
load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")


app = FastAPI(title="Dashboard Media Center")

# Configuração de CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, você pode restringir ao IP do seu celular ou painel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChannelRequest(BaseModel):
    url: str

def kill_current_media():
    """Encerra processos de vídeo abertos para evitar sobreposição de áudio/vídeo."""
    os.system("killall -9 vlc cvlc 2>/dev/null")
    os.system("pkill -9 -f chromium 2>/dev/null")

def get_display_env():
    """Garante que as aplicações abram na tela da TV conectada ao servidor."""
    return dict(os.environ, DISPLAY=":0")

@app.post("/play/camera")
def play_camera():
    kill_current_media()
    
    if not RTSP_URL:
        return {"error": "URL da câmera não configurada no .env"}
        
    subprocess.Popen(
        ["/snap/bin/vlc", "--fullscreen", "--no-osd", "--no-video-title-show" ,RTSP_URL],
        env=get_display_env()
    )
    return {"status": "Câmera iniciada"}

@app.post("/play/iptv")
def play_iptv(request: ChannelRequest):
    kill_current_media()
    
    subprocess.Popen(
        ["cvlc", "--fullscreen", "--no-osd", "--no-video-title-show", "--aout=alsa", "--alsa-audio-device=plughw:0,3", request.url],
        env=get_display_env()
    )
    return {"status": f"Canal iniciado: {request.url}"}

@app.post("/play/youtube")
def play_youtube():
    kill_current_media()
    
    ua_tv = "Mozilla/5.0 (SMART-TV; Linux; Tizen 5.0) AppleWebKit/538.1 (KHTML, like Gecko) Version/5.0 NativeTV/5.0.0"
    
    subprocess.Popen([
        "chromium",
        "--kiosk",
        "--disable-infobars",
        f"--user-agent={ua_tv}",
        "https://www.youtube.com/tv"
    ], env=get_display_env())
    
    return {"status": "YouTube Smart TV iniciado"}

@app.post("/stop")
def stop_media():
    """Rota de segurança para limpar a tela e interromper qualquer mídia."""
    kill_current_media()
    return {"status": "Mídia encerrada"}
