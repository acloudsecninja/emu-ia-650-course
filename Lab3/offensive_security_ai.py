#!/usr/bin/env python3
"""
Offensive Security Testing with Hugging Face AI Models
Author: Security Research Lab
Description: Python script for testing offensive security tactics using Hugging Face AI models
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from typing import List, Dict, Any
from datetime import datetime

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install requirements: pip install -r requirements.txt")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('offensive_security_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
console = Console()

class OffensiveSecurityAI:
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", device: str = "auto"):
        """
        Initialize the Offensive Security AI testing framework
        
        Args:
            model_name: Hugging Face model name
            device: Device to run model on (auto, cpu, cuda)
        """
        self.model_name = model_name
        self.device = self._determine_device(device)
        self.tokenizer = None
        self.model = None
        self.generator = None
        self.target_os = "windows"
        self.attack_results = []
        
    def _determine_device(self, device: str) -> str:
        """Determine the best device for model inference"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        return device
    
    def load_model(self):
        """Load the Hugging Face model and tokenizer"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Loading model and tokenizer...", total=None)
                
                logger.info(f"Loading model: {self.model_name}")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                    device_map="auto" if self.device == "cuda" else None
                )
                
                if self.device == "cpu":
                    self.model = self.model.to(self.device)
                
                # Set padding token if not present
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.generator = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    device=0 if self.device == "cuda" else -1,
                    max_length=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                progress.update(task, description="Model loaded successfully!")
                
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def generate_attack_vectors(self, attack_type: str, target_info: Dict[str, Any]) -> List[str]:
        """
        Generate attack vectors using AI model
        
        Args:
            attack_type: Type of attack (phishing, payload, recon, etc.)
            target_info: Information about the target system
            
        Returns:
            List of generated attack vectors
        """
        prompts = {
            "phishing": f"Generate realistic phishing email templates targeting {target_info.get('company', 'organization')} employees. The target OS is {self.target_os}. Focus on social engineering tactics.",
            "payload": f"Create obfuscated PowerShell payloads for {self.target_os} systems that could bypass common antivirus solutions. Include various techniques.",
            "recon": f"Suggest reconnaissance commands and techniques for gathering information about {self.target_os} networks and systems.",
            "privilege_escalation": f"Generate privilege escalation techniques and commands for {self.target_os} systems.",
            "lateral_movement": f"Create methods for lateral movement across {self.target_os} systems in a network.",
            "persistence": f"Suggest persistence mechanisms for maintaining access to {self.target_os} systems."
        }
        
        prompt = prompts.get(attack_type, f"Generate security testing techniques for {self.target_os} systems.")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Generating attack vectors...", total=None)
                
                results = self.generator(
                    prompt,
                    max_length=500,
                    num_return_sequences=3,
                    temperature=0.8,
                    pad_token_id=self.tokenizer.eos_token_id
                )
                
                attack_vectors = [result['generated_text'] for result in results]
                progress.update(task, description="Attack vectors generated!")
                
            return attack_vectors
            
        except Exception as e:
            logger.error(f"Failed to generate attack vectors: {e}")
            return []
    
    def scan_target(self, target_ip: str, scan_type: str = "basic") -> Dict[str, Any]:
        """
        Perform network reconnaissance on target
        
        Args:
            target_ip: Target IP address
            scan_type: Type of scan (basic, comprehensive, stealth)
            
        Returns:
            Scan results dictionary
        """
        scan_results = {
            "target": target_ip,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        try:
            if scan_type == "basic":
                # Basic ping test
                result = subprocess.run(
                    ["ping", "-n", "4", target_ip],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                scan_results["results"]["ping"] = {
                    "success": result.returncode == 0,
                    "output": result.stdout
                }
            
            elif scan_type == "comprehensive":
                # Port scan using nmap (if available)
                try:
                    result = subprocess.run(
                        ["nmap", "-sS", "-O", target_ip],
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    scan_results["results"]["nmap"] = {
                        "success": result.returncode == 0,
                        "output": result.stdout
                    }
                except FileNotFoundError:
                    logger.warning("nmap not found, skipping port scan")
                    scan_results["results"]["nmap"] = {
                        "success": False,
                        "output": "nmap not available"
                    }
            
            logger.info(f"Scan completed for {target_ip}")
            return scan_results
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            scan_results["error"] = str(e)
            return scan_results
    
    def test_payload(self, payload: str, target_type: str = "test") -> Dict[str, Any]:
        """
        Test generated payload in a safe environment
        
        Args:
            payload: The payload to test
            target_type: Type of target (test, sandbox, etc.)
            
        Returns:
            Test results dictionary
        """
        test_results = {
            "payload": payload,
            "target_type": target_type,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        # For safety, we'll analyze the payload structure without execution
        try:
            # Analyze payload characteristics
            test_results["results"]["analysis"] = {
                "length": len(payload),
                "contains_powershell": "powershell" in payload.lower(),
                "contains_base64": "base64" in payload.lower() or any(c.isupper() and c.islower() and c.isdigit() for c in payload),
                "suspicious_commands": self._detect_suspicious_commands(payload)
            }
            
            logger.info(f"Payload analysis completed")
            return test_results
            
        except Exception as e:
            logger.error(f"Payload testing failed: {e}")
            test_results["error"] = str(e)
            return test_results
    
    def _detect_suspicious_commands(self, payload: str) -> List[str]:
        """Detect potentially suspicious commands in payload"""
        suspicious_patterns = [
            "invoke-expression",
            "iex",
            "downloadstring",
            "reflection.assembly",
            "rundll32",
            "regsvr32",
            "certutil",
            "bitsadmin"
        ]
        
        found = []
        payload_lower = payload.lower()
        for pattern in suspicious_patterns:
            if pattern in payload_lower:
                found.append(pattern)
        
        return found
    
    def generate_report(self, output_file: str = "security_test_report.json"):
        """Generate comprehensive security test report"""
        report = {
            "test_metadata": {
                "timestamp": datetime.now().isoformat(),
                "model_used": self.model_name,
                "device": self.device,
                "target_os": self.target_os
            },
            "attack_results": self.attack_results,
            "summary": {
                "total_tests": len(self.attack_results),
                "successful_tests": sum(1 for r in self.attack_results if r.get("success", False))
            }
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Report saved to {output_file}")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return None
    
    def display_results(self):
        """Display test results in a formatted table"""
        if not self.attack_results:
            console.print("[yellow]No attack results to display[/yellow]")
            return
        
        table = Table(title="Offensive Security Test Results")
        table.add_column("Attack Type", style="cyan")
        table.add_column("Target", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Timestamp", style="blue")
        
        for result in self.attack_results:
            status = "✓ Success" if result.get("success", False) else "✗ Failed"
            table.add_row(
                result.get("attack_type", "Unknown"),
                result.get("target", "Unknown"),
                status,
                result.get("timestamp", "Unknown")
            )
        
        console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Offensive Security Testing with AI Models")
    parser.add_argument("--model", default="microsoft/DialoGPT-medium", help="Hugging Face model name")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP address")
    parser.add_argument("--attack-type", choices=["phishing", "payload", "recon", "privilege_escalation", "lateral_movement", "persistence"], 
                       default="payload", help="Type of attack to generate")
    parser.add_argument("--scan-type", choices=["basic", "comprehensive", "stealth"], 
                       default="basic", help="Type of reconnaissance scan")
    parser.add_argument("--output", default="security_test_report.json", help="Output report file")
    parser.add_argument("--device", choices=["auto", "cpu", "cuda"], default="auto", help="Device to run model on")
    
    args = parser.parse_args()
    
    try:
        # Initialize the AI security testing framework
        ai_security = OffensiveSecurityAI(model_name=args.model, device=args.device)
        
        console.print("[bold green]🔐 Offensive Security AI Testing Framework[/bold green]")
        console.print(f"Model: {args.model}")
        console.print(f"Target: {args.target}")
        console.print(f"Attack Type: {args.attack_type}")
        
        # Load the model
        ai_security.load_model()
        
        # Perform reconnaissance
        console.print("\n[bold yellow]🔍 Performing reconnaissance...[/bold yellow]")
        scan_results = ai_security.scan_target(args.target, args.scan_type)
        
        # Generate attack vectors
        console.print(f"\n[bold yellow]⚡ Generating {args.attack_type} attack vectors...[/bold yellow]")
        target_info = {"company": "Target Organization", "os": "Windows"}
        attack_vectors = ai_security.generate_attack_vectors(args.attack_type, target_info)
        
        # Test payloads
        console.print("\n[bold yellow]🧪 Testing generated payloads...[/bold yellow]")
        for i, vector in enumerate(attack_vectors):
            test_result = ai_security.test_payload(vector, "sandbox")
            test_result["attack_type"] = args.attack_type
            test_result["target"] = args.target
            test_result["success"] = test_result.get("error") is None
            ai_security.attack_results.append(test_result)
            
            console.print(f"  • Test {i+1}: {'✓' if test_result.get('success', False) else '✗'}")
        
        # Display results
        console.print("\n[bold blue]📊 Test Results:[/bold blue]")
        ai_security.display_results()
        
        # Generate report
        console.print(f"\n[bold green]📄 Generating report: {args.output}[/bold green]")
        ai_security.generate_report(args.output)
        
        console.print("\n[bold green]✅ Security testing completed![/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Testing interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")
        logger.error(f"Main execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
