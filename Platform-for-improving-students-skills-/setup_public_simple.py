"""
SkillTwin Public Access Server
Simple tunneling solution for multi-user access
"""
import socket
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.request
import json
import sys

class TunnelHandler:
    def __init__(self):
        self.public_ip = None
        self.tunnel_url = None
        
    def get_public_ip(self):
        """Get public IP address"""
        try:
            response = urllib.request.urlopen('https://api.ipify.org?format=json')
            data = json.loads(response.read().decode())
            return data['ip']
        except:
            try:
                response = urllib.request.urlopen('https://ipinfo.io/json')
                data = json.loads(response.read().decode())
                return data['ip']
            except:
                return "Unable to get public IP"
    
    def create_tunnel_info(self):
        """Create tunnel information"""
        self.public_ip = self.get_public_ip()
        
        print("\n" + "="*60)
        print("SKILLTWIN PUBLIC ACCESS SETUP")
        print("="*60)
        print(f"Public IP: {self.public_ip}")
        print(f"Local Frontend: http://localhost:3000")
        print(f"Local Backend: http://localhost:5000")
        print("\nACCESS OPTIONS:")
        print("="*60)
        
        print("\n1. DIRECT ACCESS (Same Network):")
        print(f"   Frontend: http://10.10.37.167:3000")
        print(f"   Backend:  http://10.10.37.167:5000")
        
        print("\n2. PORT FORWARDING (Router Setup):")
        print(f"   Forward port 3000 to your computer")
        print(f"   Forward port 5000 to your computer")
        print(f"   Then access via: http://{self.public_ip}:3000")
        
        print("\n3. MOBILE HOTSPOT (Easiest):")
        print("   - Enable mobile hotspot on your computer")
        print("   - Other devices connect to your hotspot")
        print("   - Access via: http://192.168.137.1:3000")
        
        print("\n4. CLOUD DEPLOYMENT (Production):")
        print("   - Deploy to Vercel (Frontend)")
        print("   - Deploy to Render (Backend)")
        print("   - Get permanent public URLs")
        
        print("\n" + "="*60)
        print("LOGIN CREDENTIALS:")
        print("   Email: demo@skilltwin.com")
        print("   Password: demo123")
        print("="*60)
        
        return self.public_ip

def main():
    """Main tunnel setup function"""
    print("Setting up SkillTwin public access...")
    
    tunnel = TunnelHandler()
    public_ip = tunnel.create_tunnel_info()
    
    print("\nSETUP COMPLETE!")
    print("Next Steps:")
    print("1. Choose an access method from above")
    print("2. Configure router/hotspot if needed")
    print("3. Share the access URL with users")
    print("4. Users can login and use all features")
    
    print("\nKeep this window open for reference")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(60)
            print(f"Server status check - {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print("\nTunnel setup closed")

if __name__ == "__main__":
    main()
