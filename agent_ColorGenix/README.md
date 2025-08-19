![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:color-adjustment](https://img.shields.io/badge/color--adjustment-3D8BD3)  

**Description**:  
The **ColorGenixServerAgent** is a lightweight autonomous agent designed to perform dynamic image enhancement by adjusting brightness, contrast, and saturation levels based on the client's request. It processes input image paths and returns updated image paths after enhancement using OpenCV. This agent is built using the `uAgents` framework and can communicate asynchronously with clients.

---

## Data Models

**Input Data Model**

```python
class ColorGenixRequest(Model):
    image_path: str         # Path to the input image
    brightness: float       # Multiplier for brightness adjustment
    contrast: float         # Multiplier for contrast adjustment
    saturation: float       # Multiplier for saturation adjustment
```

**Output Data Model**

```python
class ColorGenixResponse(Model):
    processed_image_path: str   # Path to the saved, processed image
```

---

## Features

- Dynamic adjustment of **brightness**, **contrast**, and **saturation**
- Leverages **OpenCV** for efficient image processing
- Asynchronous agent-to-agent communication via `uAgents`
- Logs and error-handling for invalid image paths
- Saves the processed image with a modified filename

---

## Components

### Agent Information
- **Name**: `ColorGenixServerAgent`
- **Port**: `5003`
- **Endpoint**: `http://localhost:5003/submit`
- **Seed**: `ColorGenixAgentSeed`
- **Responsibilities**:  
  - Receives image processing requests  
  - Applies color adjustments using OpenCV  
  - Saves and returns the processed image path to the client agent  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework  
- OpenCV (`cv2`) and NumPy

Install dependencies:

```bash
pip install uagents opencv-python numpy
```

### Running of the agent 

Ensure the image paths passed are **absolute or correctly relative** paths and are accessible.  
Start the agent using:

```bash
python <filename>.py
```

This will launch the `ColorGenixServerAgent` on port `5003` and listen for requests.

---

## Client Code

To communicate with this agent, a client agent needs to send a `ColorGenixRequest` with the required image parameters to:

```python
CLIENT_AGENT_ADDRESS = "agent1qd3v4vsy7tgtqslv06t07xva8q8rd29p82f4ckz9r44nh7r3myyhkdxvvj8"
```

Expected response will be a `ColorGenixResponse` containing the path of the processed image.

---

## Information about an agent

- The processed image is saved in the **same directory** as the input image, with a prefix `processed_` added to the filename.
- The color adjustments are applied in HSV space (for saturation), then BGR space (for brightness & contrast).
- The system logs errors if the image is unreadable or the path is incorrect.

---

## Future Enhancements

- Add support for batch image processing  
- Implement real-time image preview (pre/post adjustment)  
- Add REST or WebSocket support for external integrations  
- Allow fine-tuning using histograms or adaptive methods  
- Integrate image format conversions (e.g., PNG to JPG)
