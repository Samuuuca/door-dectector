// Substitua pelo IP real do seu Ubuntu Server
const API_URL = "http://192.168.0.XXX:8000";

async function sendCommand(endpoint, body = null) {
    try {
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (body) {
            options.body = JSON.stringify(body);
        }

        const response = await fetch(`${API_URL}${endpoint}`, options);
        const data = await response.json();
        console.log("Comando enviado com sucesso:", data);
        
    } catch (error) {
        console.error("Erro na comunicação:", error);
        alert("Falha de conexão com o servidor da TV.");
    }
}

// Controle do Modal de TV
function openModal() {
    const modal = document.getElementById('tvModal');
    modal.classList.remove('hidden');
}

function closeModal() {
    const modal = document.getElementById('tvModal');
    modal.classList.add('hidden');
}

// Funções de Mídia
function playCamera() {
    sendCommand("/play/camera");
}

function playIPTV(canalUrl) {
    // Envia a requisição com o link específico e fecha o modal
    sendCommand("/play/iptv", { url: canalUrl });
    closeModal();
}

function playYouTube() {
    sendCommand("/play/youtube");
}

function stopMedia() {
    sendCommand("/stop");
}