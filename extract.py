import yt_dlp
import os



def download_youtube_video(url, output_path='downloads'):

    def open_video(file_path):
        os.startfile(file_path)
        video_file = os.path.join(output_path)
        open_video(video_file)
    try:
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'noplaylist': True  # corrected key name
        }

        print(f'Attending to download: {url}')
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f'Download complete! Video saved to {filename}')
            return {
                "filename": filename,
                "title": info.get("title"),
                "url": url
            }

    except yt_dlp.utils.DownloadError as de:
        print(f'Download error! {str(de)}')
        print('\nListing available formats...')

        try:
            with yt_dlp.YoutubeDL({'listformats': True}) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f'Failed to list formats: {str(e)}')
            
        return None

if __name__ == '__main__':
    video_url = input('Enter url: ')
    download_youtube_video(video_url)
