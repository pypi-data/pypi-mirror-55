import clyngor

for i in next(clyngor.ASP('a(1). #show a/1.').int_not_parsed):
    print(i[1][0]+ "a")