# Video 2 transcript

[Watch Video 2 on YouTube](https://www.youtube.com/watch?v=MQvJQ_6Ged4)

0:033 secondsAll righty. This is my second video.
0:066 secondsThis will be my project to code walkthrough. This is kind of all code on here that I have. Um, I used
0:1515 secondsOpenAI and Codeex to implement the app and write the verification checks inside of this project. And this is my app tree
0:2424 secondsthat I have in project folder.
0:5050 secondsbe my prices.
0:5252 secondsSo, as you can see here, the application kind of starts with monthly adjusted closes for VI LQD and BT. Um, the parser
1:021 minute, 2 secondschecks that months are consecutive and prices are positive.
1:101 minute, 10 secondsLet me switch over to here portfolio.
1:231 minute, 23 secondsI'm going to go to my estimate here.
1:281 minute, 28 secondsUh each monthly return is the current divided price by the previous price minus one. And the function annualizes
1:361 minute, 36 secondsthe average returns and sample volatilities and calculates the correlations used in the coariance matrix.
1:431 minute, 43 secondsAnd then we just go down to returns here. You can see that formula is right here
1:571 minute, 57 secondsand then the estimates are below it.
2:002 minutesOkay. And then we open decision here.
2:142 minutes, 14 secondsGood.
2:242 minutes, 24 secondsOkay. So here you can see the target is the scenario inflation plus 03. Um the decision function adds three percentage
2:312 minutes, 31 secondspoints to planning CPI to get the the net return hurdle and it subtracts the annual cost from gross return and checks
2:382 minutes, 38 secondseach candidate for full investment long only weights the fund cap 5day liquidity
2:452 minutes, 45 secondsvolatility and net return here right here.
2:582 minutes, 58 secondsOkay.
3:003 minutesAnd it searches in five percentage point increments and picks the lowest volatility mix that passes every rule.
3:063 minutes, 6 secondsIt also tracks the highest net return among mixes that pass the other rules. So that number helps explain a stop.
3:163 minutes, 16 secondsAnd then here are the rules lines I have here. You have fully invested, long only fun, 5day liquidity, volatility ceiling, and net return here.
3:533 minutes, 53 secondsAnd then these are the return portfolios. I know this is let me get the app open here.
4:064 minutes, 6 secondsStop share.
4:284 minutes, 28 secondsOkay. And then here you can see the app and the app shows that the results alongside the equal weight inverse volatility and 60/40 benchmark.
4:374 minutes, 37 secondsUm the first table shows the weights and estimates here
4:454 minutes, 45 secondsand then the second shows the pass or fail result for each rule.
4:504 minutes, 50 secondsOkay, here we go.
5:015 minutes, 1 secondI'm going to scroll to required stress runs now.
5:075 minutes, 7 secondsSo the same decision function runs the required stresses for the equity estimate look back window cost
5:145 minutes, 14 secondsconstraints and liquidity. The archived rate reading flags a duration review. So I use the verification suite to check
5:215 minutes, 21 secondsthe source prices known portfolio results and the app's behavior when the window changes or the BT becomes unavailable. as you can see here.
5:395 minutes, 39 secondsAnd then I also did pre-open the verification check in uh Visual Studio Code. So I'll just pull that up now.
5:575 minutes, 57 secondsYeah. Okay. And you can see all of these are passing here
6:076 minutes, 7 secondsfor the verification of the project. So that's kind of just me going over my code and a little bit more of the app.
6:166 minutes, 16 secondsThat will mark the end of video two.

