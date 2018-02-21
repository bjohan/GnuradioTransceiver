
module speaker(){
    color([0.3, 0.3, 0.3]){
        translate([0,0,5]){
            cylinder(3, 20, 20);
            translate([0,0,3])
                cylinder(10, 37/2, 32/2);
            translate([0,0,13])
                cylinder(7,22/2, 22/2);
        }
    }
}

module speakerHole(){
    speaker();
    translate([0,0,-5])
    cylinder(10, 18, 18);
    
}


module speakerSlot(){
    //hull(){
        minkowski(){
        speakerHole();
        cube([0.5, 100.5, 0.5]);    
        //translate([0,100, 0])
        //    speakerHole();
    }
}
//speakerWithHole();

module tube(l, ri, ro){
    difference(){
        cylinder(l, ro, ro);
        translate([0,0,-0.1])
        cylinder(l+0.2, ri, ri);
    }
}

module speakerGrill(d){
    translate([0,0,-d]){
        tube(d, 3,5);
        tube(d, 10,12);
        tube(d, 18,20);
        //translate([11, 0, 0])
        //    tube(d, 6, 8);
        translate([0, 11, 0])
            tube(d, 6, 8);
        //translate([-11, 0, 0])
        //    tube(d, 6, 8);
        translate([0, -11, 0])
            tube(d, 6, 8);
    }
}

module speakerGrillHoles(d){
    //speakerGrill(d+0.2);
    difference(){
        translate([0,0,-d])
            cylinder(d, 20, 20);
            translate([0,0,0.1])
                speakerGrill(d+0.2);
    }
}

