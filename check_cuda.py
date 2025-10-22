"""Quick CUDA verification script"""
import torch

print('=' * 60)
print('PyTorch CUDA Verification')
print('=' * 60)
print(f'PyTorch version: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA version: {torch.version.cuda}')
print(f'cuDNN version: {torch.backends.cudnn.version()}')
print(f'Number of GPUs: {torch.cuda.device_count()}')

if torch.cuda.is_available():
    print(f'GPU 0: {torch.cuda.get_device_name(0)}')
    props = torch.cuda.get_device_properties(0)
    print(f'GPU Memory: {props.total_memory / 1024**3:.2f} GB')
    print(f'Compute Capability: {props.major}.{props.minor}')
else:
    print('WARNING: CUDA is not available!')

print('=' * 60)
