import streamlit as st
import os
import time
import subprocess
from pytube import Playlist, YouTube
import yt_dlp

# ==============================
# 🔧 Funções utilitárias
# ==============================

def verificar_dependencias():
    """Verifica se ffmpeg e yt-dlp estão instalados e atualizados."""
    st.subheader("🧩 Verificação de dependências")

    # Verificar ffmpeg
    ffmpeg_instalado = False
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        ffmpeg_instalado = True
        st.success("✅ ffmpeg encontrado!")
    except Exception:
        st.error("❌ ffmpeg não encontrado. É necessário para juntar vídeo + áudio.")
        st.info("💡 Instale em: https://www.gyan.dev/ffmpeg/builds/ (adicione ao PATH do sistema).")

    # Verificar atualização do yt-dlp
    try:
        yt_dlp_version = subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        current_version = yt_dlp_version.stdout.strip()
        st.info(f"📦 Versão atual do yt-dlp: `{current_version}`")

        # Testar atualização
        st.write("🔍 Verificando atualizações do yt-dlp...")
        subprocess.run(["yt-dlp", "-U"], capture_output=True, text=True)
        st.success("✅ yt-dlp está atualizado!")
    except Exception:
        st.error("❌ yt-dlp não encontrado. Instale com: `pip install -U yt-dlp`")

    return ffmpeg_instalado


def obter_videos_playlist(playlist_url):
    """Obtém uma lista de vídeos (objeto pytube.YouTube) a partir de uma playlist."""
    try:
        playlist = Playlist(playlist_url)
        playlist._video_regex = r"\"url\":\"(/watch\?v=[\w-]*)"
        videos = [YouTube(url) for url in playlist.video_urls]
        return videos
    except Exception as e:
        st.error(f"Erro ao obter vídeos da playlist: {e}")
        return []


def baixar_videos(videos, pasta_destino):
    """Baixa os vídeos da lista usando yt_dlp."""
    total = len(videos)
    if total == 0:
        st.warning("Nenhum vídeo encontrado para download.")
        return

    progress_bar = st.progress(0)
    status_text = st.empty()

    for i, video in enumerate(videos):
        try:
            status_text.text(f"🎬 Baixando: {video.video_id}...")
            VIDEO_URL = f'https://www.youtube.com/watch?v={video.video_id}'
            ydl_opts = {
                'format': 'best[height<=720]',
                'outtmpl': os.path.join(pasta_destino, '%(title)s.%(ext)s'),
                'quiet': True,
                'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'},
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([VIDEO_URL])
        except Exception as e:
            st.error(f"❌ Erro ao baixar {video.video_id}: {e}")

        progress = int(((i + 1) / total) * 100)
        progress_bar.progress(progress)
        time.sleep(0.2)

    status_text.text("✅ Todos os vídeos foram baixados!")
    st.success(f"Vídeos salvos em: {pasta_destino}")
    st.balloons()

# ==============================
# 🧩 Interface Streamlit
# ==============================

st.set_page_config(page_title="YouTube Playlist Downloader", page_icon="🎬", layout="centered")

st.title("🎬 YouTube Playlist Downloader")
st.markdown("Baixe todos os vídeos de uma playlist do YouTube com apenas um clique!")

# 1️⃣ Verificação de dependências
ffmpeg_ok = verificar_dependencias()

# 2️⃣ Inserir link da playlist
playlist_url = st.text_input("📋 Cole o link da playlist do YouTube:")

videos = []

# 3️⃣ Obter lista de vídeos
if playlist_url:
    with st.spinner("🔍 Obtendo vídeos da playlist..."):
        videos = obter_videos_playlist(playlist_url)
        
    if videos:
        st.success(f"✅ {len(videos)} vídeos encontrados!")
        for i, video in enumerate(videos):
            st.write(f"- {video.video_id}")
    else:
        st.error("⚠️ Nenhum vídeo encontrado ou link inválido.")

# 4️⃣ Escolher pasta de download
pasta_destino = st.text_input(
    "📁 Digite o caminho onde deseja salvar os vídeos:",
    value=os.getcwd(),
)

# 5️⃣ Iniciar download
if st.button("⬇️ Iniciar Download"):
    if not ffmpeg_ok:
        st.error("🚫 ffmpeg não encontrado. Instale antes de continuar.")
    elif not playlist_url:
        st.error("❌ Insira o link da playlist primeiro.")
    elif not videos:
        st.error("⚠️ Nenhum vídeo carregado.")
    elif not os.path.exists(pasta_destino):
        st.error("🚫 O diretório informado não existe.")
    else:
        st.info("🚀 Iniciando download...")
        baixar_videos(videos, pasta_destino)
