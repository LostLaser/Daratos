import csv
import sys
import os

def main():
    if os.path.exists('start_points/'+str(sys.argv[1]).split('.')[0]+'.txt'):
        start_point_file = open('start_points/'+str(sys.argv[1]).split('.')[0]+'.txt','r')
        stop_point = str(start_point_file.readline())
    else:
        stop_point = "1"
    print('Previous stop point is ' + stop_point + '.')
    inp_num = str(input('Press enter if you want to start here or enter a different number: '))
    if inp_num == "":
        start_point = int(stop_point)
    else:
        start_point = int(inp_num)

    char_list = ['s','d','f','q','i']
    read_file = open(str(sys.argv[1]), encoding='utf8', errors='replace')
    read_cursor = csv.reader(read_file)
    write_file = open('out_file.csv', encoding='utf8', mode='a', newline='')
    write_cursor = csv.writer(write_file, delimiter=',')
    

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
                file_out = open('start_points/'+str(sys.argv[1]).split('.')[0]+'.txt','w+')
                file_out.write(str(line_count))
                file_out.close()
                read_file.close()
                write_file.close()
                break
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