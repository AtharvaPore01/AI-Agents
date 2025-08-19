![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:image-sharpening](https://img.shields.io/badge/image--sharpening-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:opencv](https://img.shields.io/badge/opencv-3D8BD3)

**Description**:  
The **SharpVisionServerAgent** is an intelligent image sharpening agent built using OpenCV and powered by the `uAgents` framework. It accepts an image and a user-defined intensity level, applies a sharpening filter, and returns the path of the sharpened output. Ideal for improving clarity, enhancing details, and pre-processing images for visual applications or machine learning pipelines.

---

## Data Models

**Input Data Model**

```python
class SharpenRequest(Model):
    image_path: str       # Full path to the input image
    intensity: float      # Sharpening intensity level (recommended range: 0.0 to 5.0)
```

**Output Data Model**

```python
class SharpenResponse(Model):
    sharpened_image_path: str   # Path to the sharpened image
    intensity: float            # Applied sharpening intensity
```

---

## Features

- Customizable **sharpening intensity** for fine-tuned results
- Uses OpenCV’s `filter2D` with a custom kernel
- Efficient and fast image sharpening operation
- Saves the sharpened output with a descriptive filename
- Robust error-handling for invalid inputs
- Asynchronous communication using the `uAgents` protocol

---

## Components

### Agent Information
- **Name**: `SharpVisionServerAgent`
- **Port**: `5004`
- **Endpoint**: `http://localhost:5004/submit`
- **Seed**: `SharpVisionAgentSeed`
- **Responsibilities**:  
  - Accept sharpening requests with image path and intensity  
  - Apply a customizable sharpening kernel using OpenCV  
  - Save and return the sharpened image path and used intensity  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework
- OpenCV and NumPy

Install dependencies:

```bash
pip install uagents opencv-python numpy
```

### Running of the agent 

Ensure the image path provided exists and is accessible.  
To launch the agent:

```bash
python <filename>.py
```

The agent will start on `port 5004` and listen for incoming sharpening requests.

---

## Client Code

Send requests to:

```python
CLIENT_AGENT_ADDRESS = "agent1qwrg987jq74xleadcdvzdjeq38x8kvx609atr4qm550mkrfkuvk0zdqaj42"
```

A `SharpenRequest` should include:
- A valid path to the target image
- A `float` value representing sharpening intensity (e.g., `1.0`, `2.5`)

The response will be a `SharpenResponse` with the sharpened image path and the confirmed intensity level used.

---

## Information about an agent  

- The sharpening kernel is dynamically modified based on the user-defined intensity (`5 + intensity`)
- The output file is saved in the same directory with the suffix `_sharpened_<intensity>`
- Recommended intensity values range from **0.0** (minimal sharpening) to **5.0** (very sharp)
- Handles both grayscale and color images
- If the input image is unreadable, the agent logs the error and does not send a response

---

## Future Enhancements

- Add support for **auto-sharpening** based on edge detection or frequency analysis
- Provide **preview capabilities** via a GUI or web layer
- Enable **batch processing** of multiple images
- Add ability to choose from **multiple sharpening kernels**
- Implement sharpening with **adaptive thresholds** based on image characteristics
  