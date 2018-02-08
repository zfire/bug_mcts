import subprocess
for i in xrange(1000):
    p = subprocess.Popen(['python', 'go.py', str(i)+'.log'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()