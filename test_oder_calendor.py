import calendar
tc = calendar.TextCalendar()

print(tc.formatmonth(2021,10))
tc.prmonth(2021,10)
'''
    October 2021
Mo Tu We Th Fr Sa Su
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 19 20 21 22 23 24
25 26 27 28 29 30 31
'''
print(tc.formatyear(2021, c=3, m=4))
tc.pryear(2021, c=3, m=4)
'''
                                           2021

      January                February                March                  April
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
             1  2  3    1  2  3  4  5  6  7    1  2  3  4  5  6  7             1  2  3  4
 4  5  6  7  8  9 10    8  9 10 11 12 13 14    8  9 10 11 12 13 14    5  6  7  8  9 10 11
11 12 13 14 15 16 17   15 16 17 18 19 20 21   15 16 17 18 19 20 21   12 13 14 15 16 17 18
18 19 20 21 22 23 24   22 23 24 25 26 27 28   22 23 24 25 26 27 28   19 20 21 22 23 24 25
25 26 27 28 29 30 31                          29 30 31               26 27 28 29 30

        May                    June                   July                  August
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
                1  2       1  2  3  4  5  6             1  2  3  4                      1
 3  4  5  6  7  8  9    7  8  9 10 11 12 13    5  6  7  8  9 10 11    2  3  4  5  6  7  8
10 11 12 13 14 15 16   14 15 16 17 18 19 20   12 13 14 15 16 17 18    9 10 11 12 13 14 15
17 18 19 20 21 22 23   21 22 23 24 25 26 27   19 20 21 22 23 24 25   16 17 18 19 20 21 22
24 25 26 27 28 29 30   28 29 30               26 27 28 29 30 31      23 24 25 26 27 28 29
31                                                                   30 31

    September               October                November               December
Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su   Mo Tu We Th Fr Sa Su
       1  2  3  4  5                1  2  3    1  2  3  4  5  6  7          1  2  3  4  5
 6  7  8  9 10 11 12    4  5  6  7  8  9 10    8  9 10 11 12 13 14    6  7  8  9 10 11 12
13 14 15 16 17 18 19   11 12 13 14 15 16 17   15 16 17 18 19 20 21   13 14 15 16 17 18 19
20 21 22 23 24 25 26   18 19 20 21 22 23 24   22 23 24 25 26 27 28   20 21 22 23 24 25 26
27 28 29 30            25 26 27 28 29 30 31   29 30                  27 28 29 30 31
'''
