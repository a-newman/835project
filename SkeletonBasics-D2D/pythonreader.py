from time import sleep

while (True): 
    sleep(1);
    with open('tmpfifo', 'r') as infile: 
        lines = infile.readlines()
        ok = sum([1 for line in lines if "failed" not in line])
        print(ok)
        print(len(lines))
