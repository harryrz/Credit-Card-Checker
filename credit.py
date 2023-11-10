def initialize():
    global latest_operation_date
    latest_operation_date = [1,1]

    global country_in_row
    country_in_row = [None,None,None]

    global cur_owed_total
    cur_owed_total = 0


    global deactivated
    deactivated = False


    global total_purchase_in_month
    total_purchase_in_month = 0

    global from_pay_bill, from_amount_owed
    from_pay_bill = False
    from_amount_owed = False








#return True if the the date 1 (tested date) is the same as date 2 (reference date) or later than date 2
def date_same_or_later(day1, month1, day2, month2):
    if(month1 > month2):
        return True
    elif(month1 == month2):
        if(day1 >= day2):
            return True
    return False



#return true if values of three strings are all different from one another
def all_three_different(c1, c2, c3):
    if(c1 == None or c2 == None or c3 == None):
        return False
    if(c1 == c2 or c1 == c3 or c2 == c3):
        return False

    deactivated = True
    return True



#update what's the nearest 3 location of purchases
def update_country(new_c):
    global country_in_row
    country_in_row[0] = country_in_row[1]
    country_in_row[1] = country_in_row[2]
    country_in_row[2] = new_c
    #print(country_in_row)




def months_require_interest(day, month):
    global latest_operation_date
    # if month <= 2:
    #     return 0
    return month - latest_operation_date[1]







def amount_owed(day, month):
    global latest_operation_date
    global cur_owed_total
    global total_purchase_in_month
    global from_pay_bill
    global from_amount_owed

    #if the check owned amount date is before the latest operational date
    if(not date_same_or_later(day, month, latest_operation_date[0], latest_operation_date[1])):
        #print("check owned amount not successful")
        return "error"


    from_amount_owed = True
    purchase(0,day,month,"DNE#&!)")
    #from_amount_owed = False
    return cur_owed_total + total_purchase_in_month








#bill will go into the oldest purhcase, possibily with interst, then to those who didn't acuring interest
def pay_bill(amount, day, month):
    global latest_operation_date
    global total_purchase_in_month
    global cur_owed_total
    global from_pay_bill
    global from_amount_owed

    '''first generate interest, then pay'''

    #if the purhcase date is before the latest operational date
    if(not date_same_or_later(day, month, latest_operation_date[0], latest_operation_date[1])):
        #print("pay bill not successful")
        return "error"



    #update interest based on when pay the bill
    from_pay_bill = True
    purchase(0,day,month,"DNE#&!)")
    #from_pay_bill = False

    if amount <= cur_owed_total:
        cur_owed_total -= amount
    else:
        amount -= cur_owed_total
        total_purchase_in_month -= amount
        cur_owed_total = 0


    #update latest operational date
    latest_operation_date[0] = day
    latest_operation_date[1] = month







def purchase(amount, day, month, country):
    global latest_operation_date
    global country_in_row
    global deactivated
    global cur_owed_total
    global total_purchase_in_month
    global from_pay_bill
    global from_amount_owed

    '''Checking validity Part: the order of arranging checking are important'''

    #if card is deactivated, no purhcase can be made
    if (deactivated and (not from_pay_bill) and (not from_amount_owed)) :
        #print("account is permanently deactivated")
        return "error"

    #update country to check if 3 diff in a row now
    if(country != "DNE#&!)"):
        update_country(country)


    #if diff three country in a row
    if(all_three_different(country_in_row[0], country_in_row[1], country_in_row[2]) and (not from_pay_bill) and (not from_amount_owed)):

        #print("purhcase not successful location")
        deactivated = True

        '''do I rly need below code????'''
        # #when the account is fraud for attempting purchase, we still need to update interest (and technically the program can only enter this block of code for 1 time
        # i = months_require_interest(day, month)
        # passMonth = False
        # if month > latest_operation_date[1]:
        #     passMonth = True
        #
        # #print("i: ", i)
        #
        # if passMonth:
        #     month_special = total_purchase_in_month * (1.05 ** (i-1))
        #     #print("month special: ", month_special)
        #     cur_owed_total *= (1.05 ** i)
        #     cur_owed_total += month_special
        #     total_purchase_in_month = 0
        #     #print("cur owed total: ", cur_owed_total)
        #
        #
        '''something something something important'''
        '''If purchase return error, it does not update date, so should I really include this line of updating date code?'''
        # #if the date is valid, update the date, if not, don't update
        # #(because regardless of date, when 3 country in row it's disabled, so we couldn't assume the date is valid for us to update interest)
        # if(date_same_or_later(day, month, latest_operation_date[0], latest_operation_date[1])):
        #     latest_operation_date[0] = day
        #     latest_operation_date[1] = month
        return "error"


    #if the purhcase date is before the latest operational date
    if(not date_same_or_later(day, month, latest_operation_date[0], latest_operation_date[1])):
        #print("purchase not successful operational date")
        return "error"









    '''interest calculating part'''



    #print("purchase in previous checking month: ", total_purchase_in_month)
    #print("total owed before update: ", cur_owed_total)

    from_pay_bill = False
    from_amount_owed = False



    i = months_require_interest(day, month)
    passMonth = False
    if month > latest_operation_date[1]:
        passMonth = True

    #print("i: ", i)

    if passMonth:
        month_special = total_purchase_in_month * (1.05 ** (i-1))
        #print("month special: ", month_special)
        cur_owed_total *= (1.05 ** i)
        cur_owed_total += month_special
        total_purchase_in_month = 0
        #print("cur owed total: ", cur_owed_total)
        total_purchase_in_month += amount


        '''need to update'''
        #print("cur owed total: ", cur_owed_total+total_purchase_in_month)
    else:
        total_purchase_in_month += amount
        #print("in month: ", total_purchase_in_month)
        #print("cur owed total: ", cur_owed_total+total_purchase_in_month)



    #update date variables
    latest_operation_date[0] = day
    latest_operation_date[1] = month












if __name__ == "__main__":
#     initialize()
#     purchase(80, 8, 1, "Canada")
#     print("Now owing:", amount_owed(8, 1))
#     purchase(80, 8, 1, "Canada")
#     pay_bill(50, 2, 2)
#     print("Now owing:", amount_owed(6, 3))
#     purchase(40, 6, 3, "Canada")
#     print("Now owing:", amount_owed(6, 3))
#     pay_bill(30, 7, 3)
#     print("Now owing:", amount_owed(7, 3))
#     print("Now owing:", amount_owed(7, 4))
#     print("Now owing:", amount_owed(1, 5))
#     purchase(40, 2, 5, "France")
#     print("Now owing:", amount_owed(2, 5))
#     print(purchase(50, 3, 5, "United States"))
#     purchase(150, 3, 5, "Canada")
#     print("Now owing:", amount_owed(1, 6))
#
#     initialize()
#     purchase(80, 8, 1, "Canada")
#     purchase(80, 7, 1, "France")
#     purchase(80, 8, 2, "United States")
#     purchase(180, 8, 7, "Canada")
#     print("Now Owing:", amount_owed(9, 10))
#
#     initialize()
#     purchase(100, 15, 12, "France")
#     purchase(10, 1, 11, "Portugol")
#     pay_bill(50, 16, 12)
#     pay_bill(50, 15, 12)
#     print("Now owing:", amount_owed(30, 12))
#
#     initialize()
#     purchase(1232, 1, 1, "Pancakes")
#     purchase(182, 30, 1, "Panama")
#     pay_bill(1414, 1, 3)
#     purchase(12, 10, 3, "Pancakes")
#     purchase(100, 1, 4, "Somewhere")
#     pay_bill(20, 1, 3)
#     purchase(10000000, 3, 4, 'Panama')
#     print("Now Owing:", amount_owed(8, 8))
#
#     initialize()
#     purchase(110, 1, 1, "France")
#     pay_bill(110, 1, 1)
#     purchase(135, 2, 3, "Mexico")
#     pay_bill(123, 3, 4)
#     purchase(12, 5, 6, "KFC")
#     pay_bill(12, 7, 8)
#     purchase(10000000000, 7, 8, "Switzerland")
#     print("Now Owing:", amount_owed(8, 8))
#
#     initialize()
#     purchase(110, 1, 1, "France")
#     purchase(30, 30, 1, "Portugol")
#     purchase(30, 1, 2, "France")
#     pay_bill(30, 10, 2)
#     purchase(60, 4, 3, "France")
#     purchase(100, 5, 4, "Canada")
#     purchase(12, 4, 4, "Portugol")
#     pay_bill(40, 1, 6)
#     pay_bill(50, 1, 7)
#     print("Now Owing:", amount_owed(12, 12))
#
#
#
#
#
#
#
#
#



    #
    # initialize()
    #
    # purchase(77, 7, 1, "Hawaii")
    # print("Now owing:", amount_owed(7, 1))   #77p
    #
    # purchase(88, 8, 2, "China")              #88p 77i
    # print("Now owing:", amount_owed(8 ,2))   #165
    #
    # print(purchase(99, 6, 2, "Mexico"))      #error 88p 77i
    # # print("lasttransd:",last_trans_day)      #8
    #
    # print("Now owing:", amount_owed(10 ,2))  #88p 77i
    #
    # print(purchase(66, 7, 3, "China"))       #error 0p 168.85i
    # # print("Purcha", total_owed[0])
    # # print("inte", total_owed[1])
    # # print("lasttransd:",last_trans_day)      #10
    #
    # print("Now owing:", amount_owed(8 ,3))   #168.85
    # # print(purchase(55, 15, 3, "Hawaii"))     #error
    # # print("lasttransd:",last_trans_day)     #8
    #
    # print("Now owing:", amount_owed(18 ,3))  #168.85
    #
    # print("Now owing:", amount_owed(1 ,4))   #177.2925
    #
    # pay_bill(100, 7, 8)                      #115.5
    # # print("Purcha", total_owed[0])
    # # print("inte", total_owed[1])
    # # print("lasttransd:",last_trans_day)
    # print("Now owing:", amount_owed(7 ,8))
 #
 #
 #
 #    initialize()
 #    purchase(80, 8, 1, "Canada")
 #    print("Now owing:", amount_owed(8, 1)) #80.0
 #    pay_bill(50, 2, 2)
 #    print("Now owing:", amount_owed(2, 2)) #30.0 (=80-50)
 #    print("Now owing:", amount_owed(6, 3)) #31.5 (=30*1.05)
 #    purchase(40, 6, 3, "Canada")
 #    print("Now owing:", amount_owed(6, 3)) #71.5 (=31.5+40)
 #    pay_bill(30, 7, 3)
 #    print("Now owing:", amount_owed(7, 3)) #41.5 (=71.5-30)
 #    print("Now owing:", amount_owed(1, 5)) #43.65375 (=1.5*1.05*1.05+40*1.05)
 #    purchase(40, 2, 5, "France")
 #    print("Now owing:", amount_owed(2, 5)) #83.65375
 #    print(purchase(50, 3, 5, "United States")) #error (3 diff. countries in
 #    # a row)
 #    print("Now owing:", amount_owed(3, 5)) #83.65375 (no change, purchase
 #    # declined)
 #    print(purchase(150, 3, 5, "Canada")) #error (card disabled)
 #    print("Now owing:", amount_owed(1, 6)) #85.8364375
 #    #(43.65375*1.05+40)
