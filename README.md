DarthCam.

Millions of visually and speech-impaired individuals struggle with real time interaction and independent navigation in their daily lives. Existing assistive technologies are often either expensive (e.g., smart glasses) or limited in features. There's a strong need for a cost-effective, intelligent system that can describe surroundings, recognize familiar faces, and enable communication through hand signs — all using just a standard webcam and AI.

Solution Overview:
An AI-powered assistant combining visual and voice intelligence:
Real-time object detection using YOLOv8
Gesture recognition via MediaPipe
Face recognition using DeepFace
Smart and interactive responses using Grok API

Innovation and Uniqueness:
Simulates smart glasses using only a laptop webcam and AI.
Combines object detection, face recognition, and gesture input.
Uses hand gestures to trigger AI descriptions and actions.
Answers user questions through real-time Grok integration.
Designed to run offline and scale to real smart glasses in the future.

Implementation Strategy:
Tech Stack: Python, YOLOv8, MediaPipe, FastAPI, JavaScript, HTML, CSS, Grok/GPT, TTS
Frontend: Built using HTML/CSS/JS for real-time webcam overlays and user interface
Backend: FastAPI handles vision processing, face recognition, and AI responses
APIs: /describe, /ask, /gesture, /login for modular interaction
Challenges: Real-time syncing, gesture accuracy, seamless voice feedback

Impact and Feasibility:
Social Impact:
Empowers visually and speech-impaired individuals with real-time assistance
Promotes inclusive tech through AI-driven accessibility
Encourages low-cost alternatives to expensive assistive devices
Feasibility:
Built using free, open-source tools and common hardware
Can run on laptops and mobile devices with minimal resources
Modular backend enables easy scaling to future AR glasses or wearables
Fully offline-capable for environments with no internet access

Conclusion:
Developed an AI-powered assistant for the visually and speech-impaired, using only a webcam and open-source tools
Integrated object detection, face recognition, hand sign reading, and AI response into one seamless system
Simulated smart glasses using a real-time, browser-based interface
Designed for accessibility, affordability, and future scalability
A step toward a more inclusive world where assistive tech is available to all










