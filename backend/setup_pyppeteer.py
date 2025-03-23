#!/usr/bin/env python3
"""
Setup script to download and install Pyppeteer's Chromium browser.
Run this script before starting the application to ensure Chromium is properly installed.
"""

import asyncio
import os
import sys
from pyppeteer.launcher import launch, Launcher


async def install_chromium():
    """Download and install Chromium browser for Pyppeteer."""
    print("Setting up Pyppeteer's Chromium browser...")
    
    try:
        # Check if a custom executable path is specified
        executable_path = os.environ.get('PYPPETEER_CHROMIUM_EXECUTABLE')
        if executable_path:
            print(f"Using custom Chromium executable from: {executable_path}")
            if not os.path.exists(executable_path):
                print(f"WARNING: Specified Chromium executable does not exist at: {executable_path}")
                print("Will attempt to download and install Chromium.")
            else:
                print("Custom Chromium executable found.")
                # Try launching with the custom executable
                browser = await launch(executablePath=executable_path, headless=True)
                await browser.close()
                print("Successfully verified custom Chromium executable.")
                return
        
        # Check if Chromium is already downloaded
        chromium_path = Launcher.path()
        if os.path.exists(chromium_path):
            print(f"Chromium is already installed at: {chromium_path}")
        else:
            print("Downloading Chromium... This may take several minutes.")
            
        # This will download Chromium if not already downloaded
        browser = await launch(headless=True)
        await browser.close()
        
        print("Chromium setup completed successfully!")
        print(f"Chromium installed at: {Launcher.path()}")
        
    except Exception as e:
        print(f"Error during Chromium setup: {str(e)}")
        print("\nTROUBLESHOOTING TIPS:")
        print("1. If you're on macOS, try: brew install chromium")
        print("2. If you're on Linux, try: sudo apt-get install chromium-browser libatk-bridge2.0-0 libgtk-3-0")
        print("3. If you have Chrome or Chromium installed, set the PYPPETEER_CHROMIUM_EXECUTABLE environment variable:")
        print("   export PYPPETEER_CHROMIUM_EXECUTABLE=/path/to/chromium")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(install_chromium())
    print("\nYou can now run the application with: uvicorn app.main:app --reload") 