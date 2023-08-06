"""人生若只如初见，何事秋风悲画扇"""
def Authentication_authority(number):
    import subprocess
    import platform
    if platform.system()=="Windows":
        cmd = "python login_quanxian.pyc -v={}".format(number)
    elif platform.system()=="Linux":
        cmd = "python3 login_quanxian.pyc -v={}".format(number)
    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding="u8",
                                shell=True)  # 在windows 下运行时为False，linux 下运行为 True
    except Exception as e:
        print(e)
    out, err = proc.communicate(timeout=12)

    print(out)
    # print(len(out))
    if "True" in out:
        print("验证身份成功")
    else:
        print("验证身份失败")


def compile_run():

    import py_compile
    py_compile.compile('login_quanxian.py')

if __name__ == '__main__':
    # compile_run()

    Authentication_authority(11166668888)


