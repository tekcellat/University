import pickle

#with open('db', 'wb') as f:
#    pickle.dump(current_db, f)

with open('db', 'rb') as f:
    current_db = pickle.load(f)

filt_st = 'год'
filt_val = 1970

def print_db(db):
    print('Фамилия             ' + u'\u2502' + '  Год')
    middle_line = u'\u2500'*20 + u'\u253c' + u'\u2500'*6
    lin_of_db = '{:20}' + u'\u2502' + '{:6d}'
    for line in db:
        print(middle_line)
        print(lin_of_db.format(line['фамилия'], line['год']))


def remove_from_db(filt_st, filt_val, db):
    filtered_db = []
    for line in db:
        if line[filt_st] == filt_val:
            filtered_db.append(line)
    for line in filtered_db:
        db.remove(line)


print_db(current_db)
print()
print()
remove_from_db(filt_st, filt_val, current_db)
with open('db', 'wb') as f:
    pickle.dump(current_db, f)
print_db(current_db)
