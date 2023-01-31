import sys
import csv

def process():

    points_required =  int(sys.argv[1]) ## Getting the points to be deducted from the command line as an argument

    ## Lists to track the points that were spent and earned by the user from the transactions
    points_earned = []
    points_spent = []

    ## Given 'transactions.csv' file is present in the same directory as the program
    with open('transactions.csv') as data_file:
        data_reader = csv.reader(data_file, delimiter=",")
        line_count = 0

        ## For each row in the file
        for row in data_reader:

            ## Ignore the header row
            if (line_count == 0):
                line_count += 1

            ## Process the transaction    
            else:
                company = row[0]
                points = int(row[1])
                timestamp = row[2]

                ## Points earned
                if (points > 0):
                    points_earned.append((company, points,timestamp))
                
                ## Points spent
                else:
                    points_spent.append((company, points,timestamp))

        ## Sort the transactions according to the timestamp
        points_earned.sort(key=lambda transaction: transaction[2])
        points_spent.sort(key=lambda transaction: transaction[2])

        ## Get current balance of points for each company based on spends already in the transactions list
        for transaction_spent in points_spent:
            company = transaction_spent[0]
            _points_spent = -1 * int(transaction_spent[1])

            for idx, transaction_earned in enumerate(points_earned):
                
                ## Stop if points already deducted fully
                if (_points_spent <= 0):
                    break
                
                _company = transaction_earned[0]
                _points_earned = int(transaction_earned[1])

                ## If same company, match and deduct points
                if (company == _company):
                    max_points = min(_points_spent, _points_earned) ## Points to be deducted based on what is left
                    temp = list(points_earned[idx])
                    temp[1] = _points_earned - max_points
                    points_earned[idx] = tuple(temp)
                    _points_spent -= max_points

        ## Deduct points for the incoming spend
        for idx, transaction in enumerate(points_earned):

            if (points_required <= 0):
                break

            _points_earned = int(transaction[1])

            max_points = min(points_required, _points_earned)
            temp = list(points_earned[idx])
            temp[1] = _points_earned - max_points
            points_earned[idx] = tuple(temp)
            points_required -= max_points

        ## Dictionary to store final points of all companies
        output_dict = {}

        ## Process all transactions and accumulate points for each company
        for transaction in points_earned:
            company = transaction[0]
            points = transaction[1]

            output_dict[company] = output_dict.get(company, 0) + points

        print(output_dict)
        return output_dict

if __name__ == "__main__":
    process()