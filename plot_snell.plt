set grid
set yrange [1:5]

coef=2
rang=0.7

plot coef - (coef-1)/(1+exp(-(x-coef**2)/rang))
