import subprocess

l8missions = ["TM", "ETM", "OLI_TIRS"]
s2tiles = ["35UNV", "44UPU"]
l8tiles = ["198030"]
dates = [""]
clouds = ["-c 0.1", ""]
exclude = ["-e", ""]
listd = ["-l", ""]
ninsp = ["--noinspire", ""]
ovwrt = ["--overwrite", ""]
output = ["-o data_s2"]

for s2 in s2tiles:
    for c in clouds:
        for e in exclude:
            for l in listd:
                for n in ninsp:
                    for o in ovwrt:
                        command = f"python fels.py {s2} S2 2017-09-20 2017-09-30 {c} {e} {l} {n} {o} -o data_s2"
                        proc = subprocess.check_output(command, stderr=subprocess.STDOUT)
                        print(f"s2tile: {s2}; clouds: {c}; exclude: {e}; list: {l}; noinspire: {n}; overwrite: {o}; result: {proc}")

