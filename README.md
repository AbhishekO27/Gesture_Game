---

# 🌧️ Gesture-Controlled Rain Drop Catcher

A fun and interactive computer vision game where you **catch falling raindrops using body movements**! This project uses **MediaPipe**, **OpenCV**, and **Pygame** to detect your gestures and control the game in real time.

---

## 🎮 Game Concept

Control a water tank using your **hip movement** detected by your webcam. Catch falling **normal drops** and **golden drops** for points. Miss a drop and you lose a life. Game over when all lives are lost.

---

## 🛠️ Features

- 🎥 Real-time gesture detection using **MediaPipe Pose**
- 🕹️ Smooth tank control using body position
- 🌟 Golden drops worth bonus points
- 🔊 Background music and catch sound effects
- 📸 Live camera feed overlay in the game
- 🎨 Custom background and assets

---

## 🧰 Tech Stack

- **Python 3.x**
- **OpenCV** – Webcam access and frame processing
- **MediaPipe** – Real-time pose detection
- **Pygame** – Game rendering, controls, and audio

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gesture-drop-catcher.git
   cd gesture-drop-catcher
   ```

2. **Install dependencies**
   ```bash
   pip install opencv-python mediapipe pygame numpy
   ```

3. **Run the game**
   ```bash
   python main.py
   ```

> ⚠️ Replace asset paths in the script (`background.jpg`, `tank.png`, `rain_drop.png`, etc.) with your own local file paths.

---

## 🎮 Controls

- 🧍‍♂️ Move left/right by shifting your body side to side
- ⏸️ Press `P` to pause/resume
- ❌ Close the window or press `ESC` to quit

---

## 📁 Assets

Make sure the following files are present in the correct paths:
- `background.jpg`
- `tank.png`
- `rain_drop.png`
- `golden_drop.png`
- `catch.wav`
- `bg_music.mp3`


---

## 🎮 Gameplay Preview

![Gameplay Preview](media1/preview.gif)




---
