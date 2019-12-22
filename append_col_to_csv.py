import csv

append_header = "comments"
append_content = "comment"


with open('sudoku_own.csv','r') as csvinput:
    with open('new.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvinput)

        all = []
        row = next(reader)
        row.append(append_header)
        all.append(row)

        for row in reader:
            row.append(append_content)
            all.append(row)

        writer.writerows(all)
