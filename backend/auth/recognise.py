import cv2
import numpy as np
import os
from backend.db import is_face_setup, mark_face_setup_complete

def AuthenticateFace():
    """Authenticate user using face recognition"""
    try:
        # Check if face is set up
        if not is_face_setup():
            return 0  # Face not set up
        
        # Check if trainer file exists
        trainer_path = 'backend/auth/trainer/trainer.yml'
        if not os.path.exists(trainer_path):
            return 0  # No trained model
        
        # Initialize face recognizer and detector
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_path)
        detector = cv2.CascadeClassifier('backend/auth/haarcascade_frontalface_default.xml')
        
        # Initialize camera
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        
        confidence_threshold = 50  # Lower is better
        attempts = 0
        max_attempts = 30  # 3 seconds at 10 FPS
        
        print("Starting face authentication...")
        
        while attempts < max_attempts:
            ret, img = cam.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                # Predict the face
                id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
                
                if confidence < confidence_threshold:
                    print(f"Face recognized with confidence: {confidence}")
                    cam.release()
                    cv2.destroyAllWindows()
                    return 1  # Success
            
            attempts += 1
        
        cam.release()
        cv2.destroyAllWindows()
        return -1  # Authentication failed
        
    except Exception as e:
        print(f"Error in face authentication: {e}")
        return -1

def SetupFaceAuth():
    """Set up face authentication by capturing face samples"""
    try:
        # Create directories if they don't exist
        os.makedirs('backend/auth/samples', exist_ok=True)
        os.makedirs('backend/auth/trainer', exist_ok=True)
        
        # Initialize camera and detector
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cam.set(3, 640)
        cam.set(4, 480)
        detector = cv2.CascadeClassifier('backend/auth/haarcascade_frontalface_default.xml')
        
        face_id = 1  # Default user ID
        count = 0
        target_samples = 30  # Number of samples to capture
        
        print("Starting face setup. Look at the camera...")
        
        while count < target_samples:
            ret, img = cam.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                count += 1
                # Save the captured image
                cv2.imwrite(f"backend/auth/samples/face.{face_id}.{count}.jpg", 
                           gray[y:y+h, x:x+w])
                print(f"Captured sample {count}/{target_samples}")
        
        cam.release()
        cv2.destroyAllWindows()
        
        if count >= target_samples:
            # Train the model
            if train_face_model():
                mark_face_setup_complete()
                return True
        
        return False
        
    except Exception as e:
        print(f"Error in face setup: {e}")
        return False

def SetupFaceAuthWithImages(image_data_list):
    """Set up face authentication using images from frontend"""
    try:
        import base64
        from io import BytesIO
        from PIL import Image
        
        # Create directories if they don't exist
        os.makedirs('backend/auth/samples', exist_ok=True)
        os.makedirs('backend/auth/trainer', exist_ok=True)
        
        detector = cv2.CascadeClassifier('backend/auth/haarcascade_frontalface_default.xml')
        face_id = 1
        count = 0
        
        print(f"Processing {len(image_data_list)} captured images...")
        
        for i, image_data in enumerate(image_data_list):
            try:
                # Remove data URL prefix
                if image_data.startswith('data:image'):
                    image_data = image_data.split(',')[1]
                
                # Decode base64 image
                image_bytes = base64.b64decode(image_data)
                image = Image.open(BytesIO(image_bytes))
                
                # Convert to OpenCV format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    count += 1
                    # Save the face region
                    face_img = gray[y:y+h, x:x+w]
                    cv2.imwrite(f"backend/auth/samples/face.{face_id}.{count}.jpg", face_img)
                    print(f"Saved face sample {count}")
                    
            except Exception as e:
                print(f"Error processing image {i}: {e}")
                continue
        
        if count >= 10:  # Need at least 10 good face samples
            # Train the model
            if train_face_model():
                mark_face_setup_complete()
                print(f"Face setup completed with {count} samples")
                return True
        
        print(f"Insufficient face samples: {count}")
        return False
        
    except Exception as e:
        print(f"Error in face setup with images: {e}")
        return False

def train_face_model():
    """Train the face recognition model"""
    try:
        path = 'backend/auth/samples'
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("backend/auth/haarcascade_frontalface_default.xml")
        
        # Get images and labels
        image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
        face_samples = []
        ids = []
        
        for image_path in image_paths:
            # Convert to grayscale
            pil_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            img_numpy = np.array(pil_image, 'uint8')
            
            # Extract ID from filename
            id = int(os.path.split(image_path)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            
            for (x, y, w, h) in faces:
                face_samples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
        
        if len(face_samples) > 0:
            recognizer.train(face_samples, np.array(ids))
            recognizer.write('backend/auth/trainer/trainer.yml')
            print("Face model trained successfully!")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error training face model: {e}")
        return False
