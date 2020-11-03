import csv

read_fname = 'essaassistance19.csv'
write_fname = 'schools_la_not_low.csv'

#counties = ['Los Angeles', 'Orange', 'San Francisco', 'San Mateo', 'Santa Clara', 'Santa Cruz' 'Alameda', 'Contra Costa', 'Marin', 'Solano']
counties = ['Los Angeles']

def main():
    with open(write_fname, 'w', newline='') as writefile:
        writer = csv.writer(writefile)
        # headers
        writer.writerow(['County', 'District', 'School', 'Assistance Status'])
        with open(read_fname, newline='') as readfile:
            reader = csv.reader(readfile)
            for _ in range(3):
                _ = next(reader) # ignores the header rows

            for row in reader:
                county = ''
                try:
                    county = row[3]
                except:
                    continue # when county == ''

                if not county in counties:
                    continue

                school = ''
                try:
                    school = row[1]
                except:
                    continue # when school == ''

                if 'Elementary' in school or 'High' in school:
                    continue # not middle school

                district = ''
                try:
                    district = row[2]
                except:
                    continue # when district == ''

                status = ''
                try:
                    status = row[6]
                except:
                    continue # when status == ''

                if status == 'CSI Low Perform':
                    continue

                writer.writerow([county,district,school,status])

if __name__ == '__main__':
    main()
