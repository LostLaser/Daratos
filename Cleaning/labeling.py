import csv
import sys

def main():
    char_list = ['s','d','f','q','i']
    read_file = open(str(sys.argv[1]), encoding='utf8', errors='replace')
    read_cursor = csv.reader(read_file)
    write_file = open('out_file.csv', encoding='utf8', mode='a', newline='')
    write_cursor = csv.writer(write_file, delimiter=',')
    start_point = int(sys.argv[2])
    if start_point < 1:
        print ('Start point too low...')
        return
    line_count = -1
    for row in read_cursor:
        line_count += 1
        label = ''
        if line_count < start_point:
            continue
        else:
            print(str(line_count)+' '+str(row[1]))
            while not label in char_list:
                label=input()
            if (label == 'q'):
                print("Return line: "+str(line_count))
                file_out = open('line_start.txt','w')
                file_out.write(str(line_count))
                file_out.close()
                read_file.close()
                write_file.close()
                break
            elif (not label == 's') or (not label == 'd') or (not label == 'f'):
                # s == left, d == neutral, f == right
                if label == 's':
                    label = 'l'
                if label == 'd':
                    label = 'n'
                if label == 'f':
                    label = 'r'  
                if label == 'i':
                    label = 'INVALID'  
                write_cursor.writerow([row[0], row[1], label])
        

if __name__ == "__main__":
    main()