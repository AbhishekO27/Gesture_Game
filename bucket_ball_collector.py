import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize Pygame for Game
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Game Variables
bucket = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 100, 100, 50)  # Bucket at bottom center
ball = pygame.Rect(np.random.randint(0, WIDTH - 20), 0, 20, 20)  # Falling ball
score = 0

# Capture Video
cap = cv2.VideoCapture(0)

running = True
while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame (mirror effect)
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Convert color (OpenCV uses BGR, MediaPipe needs RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect body movement
    result = pose.process(rgb_frame)

    # Detect body position
    if result.pose_landmarks:
        # Get the left and right hip positions
        left_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = result.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

        # Calculate center of the hips
        x_body = int(((left_hip.x + right_hip.x) / 2) * WIDTH)

        # Move the bucket based on the body x-position
        bucket.x = max(0, min(WIDTH - bucket.width, x_body))

    # Draw the game elements
    screen.fill((30, 30, 30))  # Background color
    pygame.draw.rect(screen, (0, 255, 0), bucket)  # Green bucket
    pygame.draw.ellipse(screen, (255, 0, 0), ball)  # Red ball

    # Ball movement
    ball.y += 5
    if ball.y > HEIGHT:  # Reset if missed
        ball.x = np.random.randint(0, WIDTH - 20)
        ball.y = 0

    # Check collision
    if bucket.colliderect(ball):
        score += 1
        ball.x = np.random.randint(0, WIDTH - 20)
        ball.y = 0

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Show webcam video
    cv2.imshow("Body Tracking", frame)

    # Update the game display
    pygame.display.flip()
    clock.tick(30)

    # Exit on keypress
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()