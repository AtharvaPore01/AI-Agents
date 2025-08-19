![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:image-cropping](https://img.shields.io/badge/image--cropping-3D8BD3)  
![tag:user-interaction](https://img.shields.io/badge/user--interaction-3D8BD3)

**Description**:  
The **CropCrafterServerAgent** enables manual image cropping via a user-interactive OpenCV interface. It allows users to select a specific region of interest (ROI) from an image and returns the path of the newly cropped image. Built using the `uAgents` framework, this agent is designed for semi-automated workflows requiring user-guided image editing.

---

## Data Models

**Input Data Model**

```python
class CropCrafterRequest(Model):
    image_path: str    # Path to the image that needs cropping
```

**Output Data Model**

```python
class CropCrafterResponse(Model):
    cropped_image_path: str   # Path to the cropped output image
```

---

## Features

- Interactive cropping with **real-time ROI selection**
- Simple, intuitive interface using **OpenCV**
- Asynchronous communication via the `uAgents` protocol
- Automatically saves the cropped output with a `_cropped` suffix
- Gracefully handles user cancelation or no selection scenarios

---

## Components

### Agent Information
- **Name**: `CropCrafterServerAgent`
- **Port**: `5002`
- **Endpoint**: `http://localhost:5002/submit`
- **Seed**: `CropCrafterAgentSeed`
- **Responsibilities**:  
  - Accept image cropping requests  
  - Display an OpenCV interface for user-driven cropping  
  - Save and return the cropped image path to the client  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework  
- OpenCV

Install dependencies:

```bash
pip install uagents opencv-python
```

### Running of the agent 

Make sure the input image is accessible on the local machine. Start the agent with:

```bash
python <filename>.py
```

You will be prompted to select a region using your mouse. Upon selection, the cropped image will be saved in the same folder as the original.

---

## Client Code

The client agent should send a request to the following address:

```python
CLIENT_AGENT_ADDRESS = "agent1qdc693f5yk49ygxvg3w9af6fyhceh8xv4hdwnmd28wkrrqtdr0h0ufw6puk"
```

A `CropCrafterRequest` must include the full path to the image.  
The response will be a `CropCrafterResponse` containing the path to the cropped output.

---

## Information about an agent 

- If no region is selected, the agent returns `None` and skips saving.
- The cropped image file will have `_cropped` appended to its name before the extension.
- The OpenCV window will remain open until a valid region is selected or the user exits.
- The system ensures the output directory exists before saving.

---

## Future Enhancements

- Add support for automated cropping using edge or face detection
- Enable non-interactive (headless) cropping based on preset coordinates
- Add annotation capabilities before saving cropped output
- Extend support to multiple crop selections per session
- Integrate with web-based frontends for remote interaction
- 