//Knob parameters
knurlR = 4/2;
knobR = 50/2;
knurlH =20;
knurlStickout = knurlR;
gripRimW = knurlR;
depth=3;
sph = 10;
lockringD = 1;

//Compuited variables
angle = atan2(knurlR*2, knobR);
nKnurl = floor(2*3.14159265*knobR/(2*knurlR));
error = 360-(nKnurl*angle);
angleAdjust = angle+error/nKnurl;
echo(nKnurl);
echo(angle);
echo(angleAdjust);
echo(nKnurl*angle);
module pill(r, l){
$fn = 20;
    hull(){
        sphere(r);
        translate([0,0,l-2*r])
            sphere(r);
    }
}

module knurling(){
    for(a=[1:nKnurl]){
       rotate([0,0,a*angleAdjust]) 
            translate([knobR,0,knurlR])
                pill(knurlR, knurlH+knurlStickout);
    }
}

module lockRing(){
    translate([0,0,knurlH/3])
    difference(){
        cylinder(knurlH/6, knobR-gripRimW, knobR-gripRimW);
        cylinder(knurlH/6, knobR-gripRimW, knobR-gripRimW-lockringD);
    }
    translate([0,0,knurlH/3+knurlH/6])
    difference(){
        cylinder(knurlH/6, knobR-gripRimW, knobR-gripRimW);
        cylinder(knurlH/6, knobR-gripRimW-lockringD, knobR-gripRimW);
    }
}

module grip(){
    difference(){
        knurling();
        cylinder(knurlH, knobR, knobR);
    }
    difference(){
        cylinder(knurlH, knobR, knobR);
        cylinder(knurlH, knobR-gripRimW, knobR-gripRimW);
    }
    lockRing();
}

module knobBody(){
    difference(){
        cylinder(knurlH, knobR-gripRimW, knobR-gripRimW);
        translate([15,0,knurlH+sph-depth])
            sphere(sph);
        lockRing();
        translate([-15,0,-sph+depth])
            sphere(sph);
        cylinder(15,3,3);
    }
}

module knobAssembly(){
    color([0,0,0]){
        grip();
        knobBody();
    }
}

knobAssembly();
