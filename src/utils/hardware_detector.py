"""
Hardware detection module for identifying GPU capabilities and TensorRT compatibility.
"""
import platform
import subprocess
from typing import Dict, Optional, List
from dataclasses import dataclass
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


@dataclass
class GPUInfo:
    """GPU information container."""
    name: str
    compute_capability: Optional[str]
    memory_total: Optional[int]  # in MB
    driver_version: Optional[str]
    cuda_version: Optional[str]


@dataclass
class HardwareInfo:
    """Complete hardware information."""
    os_name: str
    os_version: str
    cpu_name: str
    has_cuda: bool
    has_tensorrt: bool
    gpus: List[GPUInfo]
    recommended_precision: str


class HardwareDetector:
    """Detects hardware capabilities for TensorRT optimization."""
    
    def __init__(self):
        self.logger = logger
        
    def detect(self) -> HardwareInfo:
        """
        Detect all hardware information.
        
        Returns:
            HardwareInfo object containing system information
        """
        self.logger.info("Starting hardware detection...")
        
        os_name = platform.system()
        os_version = platform.version()
        cpu_name = platform.processor() or platform.machine()
        
        has_cuda = self._check_cuda()
        has_tensorrt = self._check_tensorrt()
        gpus = self._detect_gpus() if has_cuda else []
        recommended_precision = self._recommend_precision(gpus)
        
        hw_info = HardwareInfo(
            os_name=os_name,
            os_version=os_version,
            cpu_name=cpu_name,
            has_cuda=has_cuda,
            has_tensorrt=has_tensorrt,
            gpus=gpus,
            recommended_precision=recommended_precision
        )
        
        self.logger.info(f"Hardware detection complete: CUDA={has_cuda}, TensorRT={has_tensorrt}")
        return hw_info
    
    def _check_cuda(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            available = torch.cuda.is_available()
            if available:
                self.logger.info(f"CUDA is available: PyTorch CUDA version {torch.version.cuda}")
            else:
                self.logger.warning("CUDA is not available")
            return available
        except Exception as e:
            self.logger.error(f"Error checking CUDA: {e}")
            return False
    
    def _check_tensorrt(self) -> bool:
        """Check if TensorRT is available."""
        try:
            import tensorrt as trt
            version = trt.__version__
            self.logger.info(f"TensorRT is available: version {version}")
            return True
        except Exception as e:
            self.logger.error(f"Error checking TensorRT: {e}")
            return False
    
    def _detect_gpus(self) -> List[GPUInfo]:
        """
        Detect GPU information using PyTorch and nvidia-smi.
        
        Returns:
            List of GPUInfo objects
        """
        gpus = []
        
        try:
            import torch
            
            if not torch.cuda.is_available():
                return gpus
            
            num_gpus = torch.cuda.device_count()
            
            # Get CUDA version
            cuda_version = torch.version.cuda or "Unknown"
            
            # Try to get driver version from nvidia-smi
            driver_version = self._get_driver_version()
            
            for i in range(num_gpus):
                props = torch.cuda.get_device_properties(i)
                
                compute_capability = f"{props.major}.{props.minor}"
                memory_mb = props.total_memory // (1024 * 1024)
                
                gpu_info = GPUInfo(
                    name=props.name,
                    compute_capability=compute_capability,
                    memory_total=memory_mb,
                    driver_version=driver_version,
                    cuda_version=cuda_version
                )
                
                gpus.append(gpu_info)
                self.logger.info(f"Detected GPU {i}: {gpu_info.name} (CC {compute_capability})")
        
        except Exception as e:
            self.logger.error(f"Error detecting GPUs: {e}")
        
        return gpus
    
    def _get_driver_version(self) -> Optional[str]:
        """Get NVIDIA driver version from nvidia-smi."""
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                return version
        except Exception:
            pass
        return None
    
    def _recommend_precision(self, gpus: List[GPUInfo]) -> str:
        """
        Recommend precision based on GPU capabilities.
        
        Args:
            gpus: List of detected GPUs
            
        Returns:
            Recommended precision: 'fp32', 'fp16', or 'int8'
        """
        if not gpus:
            return "fp32"
        
        # Get the first GPU's compute capability
        gpu = gpus[0]
        
        if gpu.compute_capability:
            major, minor = map(int, gpu.compute_capability.split('.'))
            
            # Turing (7.5) and newer support INT8 well
            if major >= 8 or (major == 7 and minor >= 5):
                return "fp16"  # Default to FP16 for good balance
            # Pascal (6.x) and newer support FP16
            elif major >= 6:
                return "fp16"
            else:
                return "fp32"
        
        return "fp16"
    
    def get_summary(self, hw_info: HardwareInfo) -> str:
        """
        Get a human-readable summary of hardware information.
        
        Args:
            hw_info: HardwareInfo object
            
        Returns:
            Formatted string summary
        """
        lines = [
            f"Operating System: {hw_info.os_name}",
            f"CPU: {hw_info.cpu_name}",
            f"CUDA Available: {'Yes' if hw_info.has_cuda else 'No'}",
            f"TensorRT Available: {'Yes' if hw_info.has_tensorrt else 'No'}",
        ]
        
        if hw_info.gpus:
            lines.append(f"\nDetected GPUs ({len(hw_info.gpus)}):")
            for i, gpu in enumerate(hw_info.gpus):
                lines.append(f"  GPU {i}: {gpu.name}")
                lines.append(f"    Compute Capability: {gpu.compute_capability}")
                lines.append(f"    Memory: {gpu.memory_total} MB")
                if gpu.driver_version:
                    lines.append(f"    Driver: {gpu.driver_version}")
                if gpu.cuda_version:
                    lines.append(f"    CUDA: {gpu.cuda_version}")
        
        lines.append(f"\nRecommended Precision: {hw_info.recommended_precision.upper()}")
        
        return "\n".join(lines)
