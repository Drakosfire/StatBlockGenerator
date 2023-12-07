import subprocess
process_call = f"node cli/process.js --input /app/my-brew.md --output /app/TerrorTurkey.html --renderer v3 --overwrite"

subprocess.run(process_call, shell=True)