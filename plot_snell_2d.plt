set pm3d map
set size ratio -1
set grid
set yrange [-10:10]
set yrange [-10:10]
set samples 100000

cff_x=2
rng_x=0.7
ref_x(x)=cff_x - (cff_x - 1) / (1 + exp(-(x - cff_x**2)/rng_x))

cff_y=2
rng_y=0.7
ref_y(y)=cff_y - (cff_y - 1) / (1 + exp(-(y - cff_y**2)/rng_y))

splot ref_x(x) + ref_y(y)
