set grid
set yrange [0:10]

sigmo=2
maxim=sqrt(10) - 1
ratio=10
logis(x)=maxim / (1 + exp( -ratio*( x - sigmo)))

ref_idx(x, s, m, r)=(m+1) - m / (1 + exp( -r*(x - s)))

ref_idx_r(x, s, m, r)=m / (1 + exp( -r*(x - s))) 
ref_idx_l(x, s, m, r)=m - m / (1 + exp( -r*(x - s)))
ref_idx_b(x, m, s0, s1, r0, r1)=m / (1 + exp( -r0*(x - s0))) - m / (1 + exp( -r1*(x - s1)))

plot ref_idx_b(x, sqrt(10.0), 2.0, 4.0, 1, 5) + ref_idx_b(x, sqrt(10.0), -4.0, -2.0, 10, 100) + 1
