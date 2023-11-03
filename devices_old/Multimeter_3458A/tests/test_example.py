import sys
sys.path.append('../')
import multimeter_3458A

def main():
    resource_name = 'GPIB0::22::INSTR'
    mm = multimeter_3458A.Multimeter_3458A(resource_name)

    mm.set_function('DCV')
    mm.set_range('DCV', '10')
    print(mm.get_data())

    mm.close()


if __name__ == "__main__":
    main()