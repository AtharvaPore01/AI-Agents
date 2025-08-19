![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:image-rotation](https://img.shields.io/badge/image--rotation-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:opencv](https://img.shields.io/badge/opencv-3D8BD3)

**Description**:  
The **RotateCrafterAgent** is an autonomous image-rotation service built with the `uAgents` framework. It receives an image and a desired rotation angle (90°, 180°, or 270°), performs the rotation using OpenCV, and returns the path to the newly rotated image. This agent is ideal for preparing image datasets or correcting image orientations programmatically.

---

## Data Models

**Input Data Model**

```python
class RotateCrafterRequest(Model):
    image_path: str    # Full path to the image
    angle: int         # Must be one of: 90, 180, or 270
```

**Output Data Model**

```python
class RotateCrafterResponse(Model):
    rotated_image_path: str   # Path to the rotated image
    angle: int                # Rotation angle applied
```

---

## Features

- Supports discrete rotation angles: **90°**, **180°**, and **270°**
- Uses OpenCV’s native rotation for high-performance processing
- Saves rotated images with angle-specific suffixes
- Error-handling for unsupported angle inputs
- Asynchronous communication via the `uAgents` framework

---

## Components

### Agent Information
- **Name**: `RotateCrafterServerAgent`
- **Port**: `5003`
- **Endpoint**: `http://localhost:5003/submit`
- **Seed**: `RotateCrafterAgentSeed`
- **Responsibilities**:  
  - Accepts image rotation instructions  
  - Performs clockwise or counter-clockwise rotation using OpenCV  
  - Stores the rotated image in the same directory  
  - Responds with the path and angle of the rotated image  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework
- OpenCV

Install required libraries:

```bash
pip install uagents opencv-python
```

### Running of the agent 

Ensure the image path exists on your machine.  
Start the agent using:

```bash
python <filename>.py
```

Once running, the agent listens on `port 5003` for rotation requests.

---

## Client Code

Clients should send a `RotateCrafterRequest` to:

```python
CLIENT_AGENT_ADDRESS = "agent1qwhwj84zyw39hxyhcclx9ka2573py5ftatc92mw2wc98tvdj6e6cjrjjwjt"
```

The request must include:
- A valid `image_path`
- A supported rotation `angle`: **90**, **180**, or **270**

On successful processing, the agent replies with a `RotateCrafterResponse` containing the path to the rotated image and the angle applied.

---

## Information about an agent  

- The output image is saved in the same folder with the suffix `_rotated_<angle>` in the filename.
- The agent currently supports only fixed-angle rotations. Unsupported angles are rejected with an error log.
- Internally uses OpenCV’s `cv2.rotate()` method for fast and accurate rotation.
- It checks for file availability and readability before attempting to process.

---

## Future Enhancements

- Add support for **arbitrary angle rotation** using affine transformations
- Enable **batch rotation** for multiple images
- Add support for **rotation with cropping or padding**
- Provide rotation previews through an optional GUI or web interface
- Extend to handle EXIF-based orientation correction for photos
