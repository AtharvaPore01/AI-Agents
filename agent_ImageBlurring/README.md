![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)  
![domain:computer-vision](https://img.shields.io/badge/computer--vision-3D8BD3)  
![tag:image-processing](https://img.shields.io/badge/image--processing-3D8BD3)  
![tag:image-blurring](https://img.shields.io/badge/image--blurring-3D8BD3)  
![tag:uagents](https://img.shields.io/badge/uagents-3D8BD3)  
![tag:opencv](https://img.shields.io/badge/opencv-3D8BD3)

**Description**:  
The **BlurCrafterServerAgent** is an asynchronous image-processing agent that applies different types of blurring techniques—Gaussian, Median, or Bilateral—based on user input. Built using the `uAgents` framework and OpenCV, this agent enhances images by smoothing them with customizable kernel sizes and responds back with the path to the newly blurred image.

---

## Data Models

**Input Data Model**

```python
class BlurRequest(Model):
    image_path: str        # Full path to the input image
    blur_type: str         # 'gaussian', 'median', or 'bilateral'
    kernel_size: int       # Size of the kernel used for blurring
```

**Output Data Model**

```python
class BlurResponse(Model):
    blurred_image_path: str   # Path to the saved blurred image
    blur_type: str            # The applied blur type
    kernel_size: int          # The kernel size used
```

---

## Features

- Supports **Gaussian**, **Median**, and **Bilateral** blurs
- Dynamically configurable **kernel size**
- File naming reflects the applied blur type
- Performs robust image I/O with validation
- Fully asynchronous message handling using `uAgents`
- Saves processed images locally with unique names

---

## Components

### Agent Information
- **Name**: `BlurCrafterServerAgent`
- **Port**: `5007`
- **Endpoint**: `http://localhost:5007/submit`
- **Seed**: `BlurCrafterAgentSeed`
- **Responsibilities**:  
  - Accept image blur requests  
  - Apply specified blur technique using OpenCV  
  - Save and return the processed image path and metadata  
  - Log meaningful errors for unsupported input or failed reads  

---

## Installation & Setup

### Prerequisites

- Python 3.7+
- `uAgents` framework
- OpenCV (`cv2`)

Install dependencies:

```bash
pip install uagents opencv-python
```

### Running of the agent 

Make sure the image path provided exists and is accessible on your local system.  
To start the agent, run:

```bash
python <filename>.py
```

---

## Client Code

To communicate with this agent, clients must send a `BlurRequest` to:

```python
CLIENT_AGENT_ADDRESS = "agent1qg548jy58678szs0sxtgtnvx62rdxpsu3kgq4wfcd3fctmkndqjwznzfr5c"
```

The request should specify:
- Valid image path
- One of the following blur types: `"gaussian"`, `"median"`, or `"bilateral"`
- Appropriate `kernel_size` (odd number recommended for most blur types)

The agent replies with a `BlurResponse` that includes the path to the blurred image, blur type, and the used kernel size.

---

## Information about an agent 

- The blurred image is saved in the **same directory** as the original with a `_blurred_<type>` suffix.
- For `gaussian` and `median`, kernel size should be **positive and odd**.
- The bilateral filter also considers spatial closeness and intensity similarity, making it edge-preserving.
- If an unsupported blur type is received, the agent gracefully skips processing and logs an error.

---

## Future Enhancements

- Add input validation for kernel size (must be odd, greater than 1)
- Support additional filters like **box blur**, **motion blur**, or **custom kernels**
- Integrate preview capability before applying blur
- Add option to save outputs in different formats (e.g., `.png`, `.webp`)
- Provide batch blurring functionality for folders or image sets
