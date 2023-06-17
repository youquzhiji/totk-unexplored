import argparse as argparse
import re

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('input', type=str)
    file=argparse.parse_args().input
    data3=[]
    #read the log file, store it in a list
    with open('log.txt', 'r') as f:
        data = f.readlines()
        f.close()
        data = [str(x) for x in data]
        print(f'Found {len(data)} lines in log.txt')
        with open(file, 'r') as f:
            data2 = f.readlines()
            f.close()
            for item in data2:
                pattern = r'\d+'  # Regex pattern to match a number string

                match = re.search(pattern, item).group()+'\n'
                if match not in data:
                    data3.append(item)
                else:
                    print(f'Removing {item}')
            with open(f'{file}-trimmed', 'w') as f:
                for item in data3:
                    f.write(item)
                f.close()


    print("done")