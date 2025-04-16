import torch

def print_torch_gpu_info():
  is_available = torch.cuda.is_available()
  if is_available:
    n_gpus = torch.cuda.device_count()
    print(f"The number of GPUs: {n_gpus}")
    for gpu_id in range(n_gpus):
      print(f"GPU ({gpu_id}): name {torch.cuda.get_device_name(0)}, address {torch.cuda.device(gpu_id)}")
    print(f"Current device id: {torch.cuda.current_device()}")
  else:
    print("No GPU is available")

if __name__ == "__main__":
  print_torch_gpu_info()
