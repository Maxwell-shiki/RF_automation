import pyvisa as visa

def main():
    rm = visa.ResourceManager()
    # print(rm.list_resources())

    print("Start to connect to Multimeter 3458A")
    # scope表示Multimeter 3458A这个设备
    scope = rm.open_resource('GPIB0::22::INSTR')
    scope.write('END ON');
    msg = scope.query('ID?')

    print(msg)
    print("")

    # scope.write("TEST")

    # print("Start to ")
    scope.write("FUNC OHM")
    scope.write('OHM 1')
    data = scope.query('READ?')
    print(data)

    err = scope.query('ERR?')
    print(err)

if __name__ == "__main__":
    main()