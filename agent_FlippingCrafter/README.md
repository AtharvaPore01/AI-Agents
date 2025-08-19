![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:image-flipping](https://img.shields.io/badge/image--flipping-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:opencv](https://img.shields.io/badge/opencv-3D8BD3)

**Description**:  
The **FlipCrafterServerAgent** provides an automated image-flipping service that supports both horizontal and vertical transformations. Designed using the `uAgents` framework, it allows clients to specify the flip direction and receive a newly saved flipped image. This lightweight agent is perfect for image augmentation workflows or preprocessing steps in computer vision pipelines.

---

## Data Models

**Input Data Model**

```python
class FlipCrafterRequest(Model):
    image_path: str       # Full path to the input image
    flip_type: str        # Options: "horizontal" or "vertical"
```

**Output Data Model**

```python
class FlipCrafterResponse(Model):
    flipped_image_path: str   # Path to the flipped image
    flip_type: str            # The flip direction used
```

---

## Features

- Flip images **horizontally** (mirror effect) or **vertically** (upside-down)
- Supports a wide range of image formats using OpenCV
- Saves output with a descriptive filename suffix
- Asynchronous communication using the `uAgents` protocol
- Built-in validation and error-handling for unsupported operations

---

## Components

### Agent Information
- **Name**: `FlipCrafterServerAgent`
- **Port**: `5004`
- **Endpoint**: `http://localhost:5004/submit`
- **Seed**: `FlipCrafterAgentSeed`
- **Responsibilities**:  
  - Accept and validate image flip requests  
  - Perform horizontal or vertical image flipping using OpenCV  
  - Save the processed image with a new filename  
  - Send the output path and flip type back to the requesting agent  

---

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- `uAgents` framework
- OpenCV library

Install dependencies:

```bash
pip install uagents opencv-python
```

### Running of the agent 

To start the agent, run the following in your terminal:

```bash
python <filename>.py
```

Make sure the image path provided in the request is valid and accessible from the machine running the agent.

---

## Client Code

This agent is designed to communicate with a client agent via:

```python
CLIENT_AGENT_ADDRESS = "agent1qtw6ryv7tmnk7ta4vf97vd9pm7g9t8scmufxxgav3jp3xq4rx9k35t30j3x"
```

Clients must send a `FlipCrafterRequest` specifying the full image path and desired `flip_type`.  
The agent will respond with a `FlipCrafterResponse` containing the path of the flipped image and the type of flip applied.

---

## Information about an agent 

- The flipped image is saved in the same directory as the original with `_flipped_<type>` added to the name.
- Accepts only `"horizontal"` or `"vertical"` as flip types; other values are rejected.
- If the image path is invalid or the image cannot be read, the agent logs the error and skips the response.
- Internally uses OpenCV's `cv2.flip()` function for efficient flipping.

---

## Future Enhancements

- Add support for **diagonal flips** and **custom flip codes**
- Integrate with a web frontend for visual flip previews
- Implement batch-flipping support for dataset preprocessing
- Extend flip control with rotation or skew options
- Add real-time flip confirmation via GUI or callback messages
