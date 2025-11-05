#!/usr/bin/env python3
import os
import sys
import subprocess
from pathlib import Path

class RhodiumDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        
    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = ['docker', 'docker-compose', 'git']
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                print(f"✅ {tool} installed")
            except:
                missing_tools.append(tool)
                print(f"❌ {tool} not installed")
        
        return missing_tools
    
    def build_docker_image(self):
        """Build Docker image"""
        print("🐳 Building Docker image...")
        try:
            subprocess.run(['docker', 'build', '-t', 'rhodium-blockchain', '.'], 
                         check=True, cwd=self.project_root)
            print("✅ Docker image built successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker build failed: {e}")
            return False
        return True
    
    def create_wallet(self):
        """Create wallet if doesn't exist"""
        wallet_file = self.project_root / 'wallet.dat'
        if not wallet_file.exists():
            print("👛 Creating new wallet...")
            try:
                subprocess.run([sys.executable, 'rhodium_wallet.py'], 
                             check=True, cwd=self.project_root)
            except subprocess.CalledProcessError as e:
                print(f"❌ Wallet creation failed: {e}")
                return False
        else:
            print("✅ Wallet already exists")
        return True
    
    def start_services(self, service=None):
        """Start services with docker-compose"""
        print("🚀 Starting Rhodium services...")
        
        compose_file = self.project_root / 'docker-compose.yml'
        cmd = ['docker-compose', '-f', str(compose_file), 'up', '-d']
        
        if service:
            cmd.append(service)
        
        try:
            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Services started successfully")
            
            # Show status
            subprocess.run(['docker-compose', '-f', str(compose_file), 'ps'], 
                         cwd=self.project_root)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start services: {e}")
            return False
        return True
    
    def stop_services(self):
        """Stop all services"""
        print("🛑 Stopping services...")
        compose_file = self.project_root / 'docker-compose.yml'
        try:
            subprocess.run(['docker-compose', '-f', str(compose_file), 'down'], 
                         check=True, cwd=self.project_root)
            print("✅ Services stopped")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to stop services: {e}")
    
    def show_status(self):
        """Show service status"""
        compose_file = self.project_root / 'docker-compose.yml'
        print("📊 Service status:")
        subprocess.run(['docker-compose', '-f', str(compose_file), 'ps'], 
                     cwd=self.project_root)
        
        print("\n🌐 Available endpoints:")
        print("   Explorer: http://localhost:5000")
        print("   P2P Node: localhost:8334")
        print("   RPC: localhost:8335")
    
    def run(self):
        """Main deployment routine"""
        print("🎉 Rhodium Blockchain Deployer")
        print("=" * 40)
        
        # Check dependencies
        missing = self.check_dependencies()
        if missing:
            print(f"\n❌ Please install: {', '.join(missing)}")
            return
        
        # Build and deploy
        if self.build_docker_image() and self.create_wallet():
            self.start_services()
            self.show_status()
            
            print("\n✅ Deployment completed!")
            print("\n🎯 Next steps:")
            print("   1. Open http://localhost:5000 for blockchain explorer")
            print("   2. Run: python3 rhodium_gui.py for GUI wallet")
            print("   3. Run: python3 rhodium_miner.py to start mining")
            print("   4. Run: ./deploy.py stop to shutdown")

def main():
    deployer = RhodiumDeployer()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'stop':
            deployer.stop_services()
        elif command == 'status':
            deployer.show_status()
        elif command == 'start':
            service = sys.argv[2] if len(sys.argv) > 2 else None
            deployer.start_services(service)
        else:
            print("Usage: ./deploy.py [stop|status|start [service]]")
    else:
        deployer.run()

if __name__ == '__main__':
    main()
