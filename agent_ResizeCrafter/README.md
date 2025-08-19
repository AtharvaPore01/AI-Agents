![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:image-resizing](https://img.shields.io/badge/image--resizing-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:opencv](https://img.shields.io/badge/opencv-3D8BD3)

**Description**:  
The **ResizeCrafterAgent** is a specialized image-processing agent that handles high-performance resizing of image files to user-specified dimensions. Built with OpenCV and powered by the `uAgents` framework, it listens for client requests, resizes images accordingly, and returns the new image path. Perfect for standardizing datasets or optimizing images for display and storage.

---

## Data Models

**Input Data Model**

```python
class ResizeCrafterRequest(Model):
    image_path: str    # Full path to the source image
    width: int         # Desired width in pixels
    height: int        # Desired height in pixels
```

**Output Data Model**

```python
class ResizeCrafterResponse(Model):
    resized_image_path: str   # Path to the saved resized image
```

---

## Features

- Resize images to **any custom dimensions**
- Uses OpenCV for **high-quality interpolation**
- Saves output with `_resized` filename suffix
- Fully asynchronous via `uAgents` communication
- Handles invalid paths and unreadable images gracefully

---

## Components

### Agent Information
- **Name**: `ResizeCrafterServerAgent`
- **Port**: `5003`
- **Endpoint**: `http://localhost:5003/submit`
- **Seed**: `ResizeCrafterAgentSeed`
- **Responsibilities**:  
  - Accept resize instructions from clients  
  - Apply image resizing using OpenCV’s `resize()` function  
  - Save the output with a new name and return the file path  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework
- OpenCV (`cv2`)

Install required dependencies:

```bash
pip install uagents opencv-python
```

### Running of the agent 

Ensure the provided image path is correct and the file is accessible locally.  
To run the agent:

```bash
python <filename>.py
```

Once started, the agent will listen on port `5003` for incoming image resize requests.

---

## Client Code

To send a resize request to the agent, target the following client address:

```python
CLIENT_AGENT_ADDRESS = "agent1qvfs476ta09v5tkvtwtwvascgwtpz5pcxxdrg0dydyl6e9cvevx3z2nyel3"
```

The request must include:
- A valid local path to the image
- Integer dimensions: `width` and `height` (in pixels)

The agent responds with a `ResizeCrafterResponse` containing the full path to the resized image.

---

## Information about an agent  

- Output file is saved in the **same directory** as the original with `_resized` added before the extension.
- If the file is not found or can't be read, the agent logs a clear error and returns `None`.
- The resizing maintains the exact width and height specified; aspect ratio is **not preserved** unless managed externally.
- OpenCV’s `cv2.resize()` uses bilinear interpolation by default for high-quality results.

---

## Future Enhancements

- Add an option to **preserve aspect ratio** with auto-scaling
- Include interpolation method selection (e.g., `INTER_LINEAR`, `INTER_CUBIC`)
- Support for **batch resizing** multiple images
- Allow resizing based on **percentage scale** rather than absolute dimensions
- Enable format conversion (e.g., `.jpg` to `.png`) during resize operation
