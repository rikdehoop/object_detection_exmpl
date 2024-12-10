import torch

# Check if CUDA is available
print("CUDA available:", torch.cuda.is_available())

# Print the installed PyTorch version
print("PyTorch version:", torch.__version__)

# Check the CUDA version used by PyTorch
print("PyTorch CUDA version:", torch.version.cuda)

# Get the number of GPUs available
print("Number of GPUs:", torch.cuda.device_count())

# Get the name of the GPU (if available)
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))


