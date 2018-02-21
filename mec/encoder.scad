module tube(l, ri, ro){
    difference(){
        cylinder(l, ro, ro);
        translate([0,0,-0.1])
        cylinder(l+0.2, ri, ri);
    }
}

module encoderScrewHoles(r,h){
    for(i=[0:2]){
        rotate([0,0,i*120])
            translate([36/2-4, 0,0])
                cylinder(h, r, r);
    }
}

module encoderShaftHole(t){
    cylinder(t,21.5/2, 21.5/2);
}

module encoderBody(){
    cylinder(36, 37/2, 37/2);
    translate([0,0,36])
        cylinder(5,20/2, 20/2);
    translate([0,0,36+5])
        cylinder(12,6/2, 6/2);
    
}

module encoderWithHoles(){
    difference(){
        encoderBody();
        translate([0,0,36-5])
            encoderScrewHoles(3/2, 6);
    }
}

encoderWithHoles();
