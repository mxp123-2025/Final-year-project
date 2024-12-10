import subprocess

def run_blender():
    # Path to Blender executable on macOS
    blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
    
    # If you want to open a specific .blend file, provide its path here
    blend_file = "cardSimulation.blender.blend"  # Replace with the actual .blend file path

    # Running Blender from the terminal using subprocess
    subprocess.run([blender_path, blend_file])

# Your script logic here

# Run Blender after the script completes
#run_blender()

blender_path = "/Applications/Blender.app/Contents/MacOS/Blender"
blend_file = "cardSimulation.blender.blend"
python_script = "test.txt"

log_file = "blender_log.txt"  # Path to your log file

command = [
    blender_path, blend_file, "--background", "--python", python_script
]

with open(log_file, "w") as log:
    subprocess.run(command, stdout=log, stderr=log)

print(f"Log saved to {log_file}")
