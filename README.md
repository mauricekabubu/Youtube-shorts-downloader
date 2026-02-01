# YouTube Downloader App

A **full-stack YouTube downloader application** built using **Python, JavaScript, HTML, CSS, Bootstrap**, and **MySQL**, designed for efficiency, security, and scalability. This app allows users to download YouTube videos and shorts seamlessly, manage their downloads, and access their history in a user-friendly dashboard.

---

## Features

### User Interface & Experience
- **Dashboard**: A clean, responsive interface built with **Bootstrap** and **CSS**, showing active downloads, history, and quick actions.
- **Downloads & History**: Users can view their downloaded videos and manage them directly from the dashboard.
- **Input Field for YouTube Links**: Simply paste the YouTube video or short URL and download instantly.
- **Automatic File Saving**: All downloads are saved automatically in a local directory for easy access.
- **Playback Option**: Users can watch previously downloaded videos directly from the history/downloads section.

### Backend & Functionality
- **Python Backend**: Handles downloading, authentication, and API requests.
- **Background Threading**: Downloads happen in the background without blocking the app’s interface.
- **JWT & Cookies**: Implements **JSON Web Tokens (JWT)** and cookies for secure session management and authentication.
- **Authorization & Security**: Ensures only authenticated users can access downloads and sensitive routes.
- **MySQL Database**: Stores user data, download history, and application settings securely.
- **API Integration**: Integrated with **SendGrid** for email notifications and alerts.

### Technical Highlights
- **Routing**: Learned and implemented multiple routes for dashboard, downloads, and authentication.
- **Threaded Downloads**: Ensures smooth user experience while downloading large videos in the background.
- **Token-Based Authentication**: Secure login and access control using JWT.
- **Extensible Backend**: Ready to implement more features like video categorization, playlists, and analytics.

---

## How It Works

1. **Paste the YouTube link** in the input field on the dashboard.
2. Click **Download**. The video download starts in the background.
3. Downloaded videos are **saved automatically** to a local folder.
4. Visit the **History/Downloads** section to:
   - Watch the downloaded videos.
   - Manage or remove past downloads.

---

## Tech Stack

- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend**: Python (Flask/other framework)
- **Database**: MySQL
- **Authentication & Security**: JWT, Cookies, Token-Based Access
- **Background Tasks**: Threading for non-blocking video downloads
- **API Integration**: SendGrid for email notifications
- **Others**: Routes, Authorization, Secure sessions

---

## Achievements

- Successfully implemented a full-stack YouTube downloader.
- Learned and applied **routes, JWT, cookies, authorization, and threading**.
- Built a **secure and responsive dashboard** with download and history functionality.
- Integrated **email APIs** for enhanced user notifications.
- Practiced **database management** with MySQL for storing user and download data.

---

## Future Goals as a Backend Developer

- Implement **scalable and robust APIs** for large-scale download management.
- Enhance **security** with advanced encryption and role-based access.
- Optimize **threading and background processing** for handling multiple downloads efficiently.
- Expand integration with **more video platforms** and cloud storage solutions.
- Build a portfolio of **secure, full-stack, and scalable applications** ready for professional backend development.

---

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-downloader-app.git
