popNum = 15;
squareSize = 1;
alpha = 0.5; // between [0, 1]
epsilon = 0.1 // between [-0.5, 0.5]
beta = 0; // Attractiveness
gamma = 0.1 // absorption coefficient [0.1, 100]

coordinates = document.getElementById("mySVG");
setCoordProperties();
setPoint(0, 0, "MainPoint");

function setPoint(x , y, pointID) {
    if (document.getElementById(pointID)) {
        document.getElementById(pointID).remove();
    }
    var svgNS = "http://www.w3.org/2000/svg";
    var point = document.createElementNS(svgNS,"circle"); //to create a circle. for rectangle use "rectangle"
    point.setAttributeNS(null,"id",pointID);
    point.setAttributeNS(null,"cx",originX + (x * squareSize));
    point.setAttributeNS(null,"cy",originY - (y * squareSize));
    point.setAttributeNS(null,"r",4);
    if (pointID == "MainPoint") {
        point.setAttributeNS(null,"fill","blue");
    } else {
        point.setAttributeNS(null,"fill","black");
    }
    point.setAttributeNS(null,"stroke","none");
    coordinates.appendChild(point);
}


// Get the position of the mouse relative to the canvas
function getMousePos(mouseEvent) {
    return {
        x: Math.round((mouseEvent.pageX - leftPos - originX) / squareSize),
        y: Math.round((topPos + originY - mouseEvent.pageY) / squareSize)
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

function addPopulation() {
    var popX;
    var popY;
    for (i = 0; i < popNum; i++) {
        popX = getRandomInteger(-150 / squareSize, 150 / squareSize)
        popY = getRandomInteger(-150 / squareSize, 150 / squareSize)
        setPoint(popX, popY, "person_" + i);
    }
}

function brightness() {
    population = [];
    for (i = 0; i < popNum; i++) {
        personCoords = getCoords("person_" + i);
        population.push({
                person: "person_" + i,
                distance: calcDistance(personCoords.x, personCoords.y, "MainPoint"),
                attraction: 0
            });
    }
    population.sort(function(a, b) {
        return (a.distance > b.distance) ? 1 : ((b.distance > a.distance) ? -1 : 0)
    });
    setColor();
}

function calcDistance(x, y, pointID) {
    MainX = getCoords(pointID).x;
    MainY = getCoords(pointID).y;
    var distance = Math.sqrt(Math.pow(x - MainX, 2) + Math.pow(y - MainY, 2));
    return distance;
}

function getCoords(pointID) {
    return {
        x: -(150 - document.getElementById(pointID).cx.baseVal.value) / squareSize,
        y: (150 - document.getElementById(pointID).cy.baseVal.value) / squareSize
    };
}

function getRandomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1) ) + min;
}

function setColor() {
    var red = [];
    var red_slide = Math.floor(255 / popNum);
    for (i = 0; i < popNum; i++) {
        red.push(255 - red_slide * i);
    }
    for (i = 0; i < popNum; i++) {
        var point = document.getElementById(population[i].person);
        point.setAttributeNS(null,"fill","rgb(" + red[i] + ", 0, 0)");
    }
}

function attract() {
    var mostAttractive = population[0].person;
    var intinsity = 10;
    //var intinsity = population[0].distance;
    var mostAttractiveX = getCoords(mostAttractive).x;
    var mostAttractiveY = getCoords(mostAttractive).y;
    for (i = 0; i < popNum; i++) {
        if (mostAttractive == population[i].person) {
            beta = 0;
            var moveX = getCoords(population[i].person).x + (alpha * epsilon);
            var moveY = getCoords(population[i].person).y + (alpha * epsilon);
            movePoint(moveX, moveY, mostAttractive);
        } else {
            distance = calcDistance(getCoords(population[i].person).x, getCoords(population[i].person).y, mostAttractive);
            beta = intinsity / (1 + (gamma * Math.pow(distance, 2)));
            var moveX = getCoords(population[i].person).x + (beta * (mostAttractiveX - getCoords(population[i].person).x)) + (alpha * epsilon);
            var moveY = getCoords(population[i].person).y + (beta * (mostAttractiveY - getCoords(population[i].person).y)) + (alpha * epsilon);
            movePoint(moveX, moveY, population[i].person);
        }
    }
    console.table(population);
}

function movePoint(moveX, moveY, pointID) {
    beforeX = getCoords(pointID).x;
    beforeY = getCoords(pointID).y;
    var point = document.getElementById(pointID);
    point.setAttributeNS(null,"cx",originX + (moveX * squareSize));
    point.setAttributeNS(null,"cy",originY - (moveY * squareSize));
    afterX = getCoords(pointID).x;
    afterY = getCoords(pointID).y;
    var lineID = pointID.replace("person", "line");
    movingLine(beforeX, beforeY, afterX, afterY, lineID);
}

function movingLine(beforeX, beforeY, afterX, afterY, lineID) {
    if (document.getElementById(lineID)) {
        document.getElementById(lineID).remove();
    }
    var svgNS = "http://www.w3.org/2000/svg";
    var line = document.createElementNS(svgNS,"line"); //to create a circle. for rectangle use "rectangle"
    line.setAttributeNS(null,"id",lineID);
    line.setAttributeNS(null,"x1",originX + (beforeX * squareSize));
    line.setAttributeNS(null,"y1",originY - (beforeY * squareSize));
    line.setAttributeNS(null,"x2",originX + (afterX * squareSize));
    line.setAttributeNS(null,"y2",originY - (afterY * squareSize));
    line.setAttributeNS(null,"stroke","black");
    line.setAttributeNS(null,"stroke-width","0.2");
    line.setAttributeNS(null,"stroke-dasharray","2");
    coordinates.appendChild(line);
}

function tryit() {
    brightness();
    attract();
}

function loop() {
    //movePoint(20, 50, "person_0");
    var i = 1;                     //  set your counter to 1

    function myLoop () {           //  create a loop function
        setTimeout(function () {    //  call a 3s setTimeout when the loop is called
            
            brightness();
            attract();          //  your code here
            i++;                     //  increment the counter
            if (i < 100) {            //  if the counter < 10, call the loop function
                myLoop();             //  ..  again which will trigger another 
            }                        //  ..  setTimeout()
        }, 200)
    }

    myLoop();
}

function refresh() {
    epsilon = document.getElementById("epsilon").value;
    alpha = document.getElementById("alpha").value;
    gamma = document.getElementById("gamma").value;
}