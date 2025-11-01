import yt_dlp
VIDEOS = [
"v=1-w1RfGIov4",
"v=BXqUH86F-kA",
"v=uzEhd3Lugik",
"v=Ptbk2af68e8",
"v=rUTKomc2gG8",
"v=FdePtO5JSd0",
"v=OmmJBfcMJA8",
"v=FjT97HVT5g8",
"v=Vbabsye7mWo",
"v=OJgu_KCCUSY",
"v=hZG9ODUdxHo",
"v=BP63NhITvao",
"v=H80nCKs9c2k",
"v=WWZX8RWLxIk",
"v=wWnBB-mZIvY",
"v=uPFasdmZHJc",
"v=cOdG4eACN2A",
"v=EEStcIe8rAM",
"v=b2K7eo5Jdj8",
"v=UXSWgnbSHxs",
"v=f5es-PpaUI8",
"v=3emz6rpcJyA",
"v=5rZqYPKIwkY",
"v=eX-lkN_Zahc",
"v=6tyHypeY4-8",
"v=oMNbc_LFz8w",
"v=mfHAQ-4Rspw",
"v=5m4UhZd-Les",
"v=XdkW62tkAgU",
"v=mc3TKp2XzhI",
"v=vEOEZ03ZyiE",
"v=slLoLLCd-k0",
"v=roP93FA-NgU"

]


for video in VIDEOS:
    VIDEO_URL = f'https://www.youtube.com/watch?{video}'
    ydl_opts = {
        'format': 'best[height<=720]',  
        'outtmpl': 'javascript/%(title)s.%(ext)s',  
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([VIDEO_URL])
    print("Download concluído!")