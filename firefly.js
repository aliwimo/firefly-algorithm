maxGeneration = 50;
population = 10;
diminsionSize = 2; // 2D
absorption = 0.1; // gamma absorption coefficient [0.1, 100]
randomness = 0.2; // alpha
attractiveness = 1; // beta at 0 distance
epsilon = 0.1 // between [-0.5, 0.5]
topLimit = 3;
downLimit = -3;
sqaureSize = 1;

//-----------------------//
populationMap = [];
distanceArray = [];
lightIntensityR = [];
attractivenessR = [];


function generateFireflies() {
    for (i = 0; i < population; i++) {
        var initX = getRandomInteger(topLimit, downLimit);
        var initY = getRandomInteger(topLimit, downLimit);
        populationMap.push({
            id: "firefly_" + i,
            locationStr: "(" + initX +", " + initY + ")",
            location: [initX, initY],
            lightIntensity: 0
        });
        setPoint(initX, initY, populationMap[i].id);
    }

    // generate random values
    function getRandomInteger(min, max) {
        return Math.floor(Math.random() * (max - min + 1) ) + min;
    }

    
}

function objectiveFunction() {
    for (i = 0; i < population; i++) {
        var sum = 0;
        for (j = 0; j < diminsionSize; j++) {
            sum += Math.pow(populationMap[i].location[j], 2);
            // sum +=  Math.pow(populationMap[i].location[j], 2);
        }
        // sum = 150 - Math.sqrt(sum);
        populationMap[i].lightIntensity = sum;
    }
}

function lightIntensityAndAttractiveness() {
    for (i = 0; i < population; i++) {
        lightIntensityR[i] = [];
        attractivenessR[i] = [];
        for (j = 0; j < population; j++) {
            var lightIntensity = 0;
            var attraction = 0;
            if ( i == j) {
                lightIntensity = 0;
                attraction = 0;
            } else {
                lightIntensity = populationMap[i].lightIntensity * Math.exp((-1 * absorption * Math.pow(distanceArray[i][j], 2)));
                attraction = attractiveness / (1 + absorption * Math.pow(distanceArray[i][j], 2));
            }
            lightIntensityR[i][j] = lightIntensity;
            attractivenessR[i][j] = attraction;
        }
    }
}

function calcDistance() {    
    //        
    for (i = 0; i < population; i++) {
        distanceArray[i] = [];
        for (j = 0; j < population; j++) {
            var distance = 0;
            if ( i == j) {
                distance = 0;
            } else {
                for (k = 0; k < diminsionSize; k++) {
                    distance += Math.pow((populationMap[i].location[k] - populationMap[j].location[k]), 2);
                }
                distance = Math.sqrt(distance);
            }
            distanceArray[i][j] = distance;
        }
    }
}

function moveTowards(id1, id2) {
    var location1 = populationMap[id1].location;
    var location2 = populationMap[id2].location;
    
    for (i = 0; i < diminsionSize; i++) {
        populationMap[id1].location[i] = location1[i] + (attractivenessR[id2][id1] * (location2[i] - location1[i])) + (randomness * epsilon);
    }
    populationMap[id1].locationStr =  "(" + populationMap[id1].location[0] +", " + populationMap[id1].location[1] + ")";
}

function moveRandomly(id) {    
    for (i = 0; i < diminsionSize; i++) {
        populationMap[id].location[i] = populationMap[id].location[i] + (randomness * epsilon);
    }
}

//---------------------------------------------//


coordinates = document.getElementById("mySVG");
setCoordProperties();

function setPoint(x , y, pointID) {
    if (document.getElementById(pointID)) {
        document.getElementById(pointID).remove();
    }
    var svgNS = "http://www.w3.org/2000/svg";
    var point = document.createElementNS(svgNS,"circle"); //to create a circle. for rectangle use "rectangle"
    point.setAttributeNS(null,"id",pointID);
    point.setAttributeNS(null,"cx",originX + (x / sqaureSize));
    point.setAttributeNS(null,"cy",originY - (y / sqaureSize));
    point.setAttributeNS(null,"r",2);
    point.setAttributeNS(null,"fill","black");
    point.setAttributeNS(null,"stroke","none");
    coordinates.appendChild(point);
}

function setCoordProperties() {
    // get the position of the coordinate element
    topPos = coordinates.getBoundingClientRect().top + window.scrollY;
    leftPos = coordinates.getBoundingClientRect().left + window.scrollX;
    
    // get the width & height of the coordinate
    bounds = coordinates.getBoundingClientRect();

    // set the origin coords
    originX = (bounds.width / 2);
    originY = (bounds.height / 2);
}

window.onresize = function(event) {
    setCoordProperties();
};

// Get the position of the mouse relative to the canvas
function getMousePos(mouseEvent) {
    return {
        x: Math.round((mouseEvent.pageX - leftPos - originX) / sqaureSize),
        y: Math.round((topPos + originY - mouseEvent.pageY) / sqaureSize)
    };
}

coordinates.addEventListener("mousemove", function (e) {
    var m = getMousePos(e);
    setInfo(m.x, "x");
    setInfo(m.y, "y");
}, false);

coordinates.addEventListener("click", function (e) {
    var m = getMousePos(e);
    setPoint(m.x, m.y, "MainPoint");
}, false);


function setInfo(position, coord) {
    infoX = document.getElementById("info"+ coord.toUpperCase());
    infoX.innerHTML = position;
}


//---------------------------------------------//

function test() {
    populationMap = [];
    generateFireflies();
    objectiveFunction();
    console.table(populationMap);
    console.log("Table1: populationMap");
    calcDistance();
    console.table(distanceArray);
    console.log("Table2: distanceArray");
    lightIntensityAndAttractiveness();
    console.table(lightIntensityR);
    console.log("Table3: lightIntensityR");
    console.table(attractivenessR);
    console.log("Table4: attractivenessR");
}


function run() {
    for (index = 0; index < population; index++) {
        var hasMoved = false;
        for (j = 0; j < population; j++) {
            if (populationMap[index].lightIntensity / 10 < lightIntensityR[index][j]) {
            // if (populationMap[index].lightIntensity < populationMap[j].lightIntensity) {
                moveTowards(index, j);
                hasMoved = true;
            }
        }
        if (hasMoved == false) {
            moveRandomly(index);
        }
    }
    
    for (i = 0; i < population; i++) {
        var initX = populationMap[i].location[0];
        var initY = populationMap[i].location[1];
        setPoint(initX, initY, populationMap[i].id);
    }
    objectiveFunction();
    lightIntensityAndAttractiveness();
    
    console.table(populationMap);
    console.log("Table1: populationMap");
    calcDistance();
    lightIntensityAndAttractiveness();
}

function loop() {
    //movePoint(20, 50, "person_0");
    var i = 1;                     //  set your counter to 1

    function myLoop () {           //  create a loop function
        setTimeout(function () {    //  call a 3s setTimeout when the loop is called
            
            run();
            i++;                     //  increment the counter
            if (i < maxGeneration) {            //  if the counter < 10, call the loop function
                myLoop();             //  ..  again which will trigger another 
            }                        //  ..  setTimeout()
        }, 200)
    }

    myLoop();
    console.log("Done!!");
}