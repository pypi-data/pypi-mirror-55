#version 3.6;

// Right-handed coordinate system in which the z-axis points upwards
camera {
	location <30,-50,25>
	sky z
	right -0.05*x*image_width/image_height
	up 0.05*z
	look_at <0,0,0>
}

// White background
background{rgb 1}

// Two lights with slightly different colors
light_source{<-8,-20,30> color rgb <0.77,0.75,0.75>}
light_source{<25,-12,12> color rgb <0.38,0.40,0.40>}

// Radius of the Voronoi cell network
#declare r=0.008;

// Voronoi cells
union{
#include "FRAME"
	pigment{rgb <1,0.4,0.45>} finish{specular 0.5 ambient 0.42}
}
