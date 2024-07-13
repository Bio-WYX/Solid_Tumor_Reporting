import subprocess as sub
def Run(command):
        try: 
            subp = sub.Popen(command,shell=True)
            subp.wait()
            if subp.poll() != 0:
                raise ValueError("oncokb api调用错误")
            else:
                pass
        except ValueError as e:
            print("引发异常：",repr(e))