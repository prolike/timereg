var button = document.getElementById('timebutton')
var button2 = document.getElementById('test')
var start = document.getElementById('res1')
var end = document.getElementById('res2')
var issueID = document.getElementById('issueID')

// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal 
button.onclick = function () {
    modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

button2.onclick = function () {
    // alert(start.value)
    // alert(end.value)

    var json = '[{ ' +
        '"storage": {' +
        '"repo": "empty", ' +
        '"issue": ' + issueID.value +
        '}, ' +
        '"content": {' +
        '"user": "davidcarl",' +
        '"state": "start",' +
        '"timestamp": "' + start.value + '"' +
        '}},' +
        '{ ' +
        '"storage": {' +
        '"repo": "empty", ' +
        '"issue": ' + issueID.value +
        '}, ' +
        '"content": {' +
        '"user": "davidcarl",' +
        '"state": "end",' +
        '"timestamp": "' + end.value + '"' +
        '}' +
        '}]'

    const url = "http://localhost:5000/api/test"
    const other = {
        method: "GET"
    }
    fetch(url, other)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            console.log(JSON.stringify(myJson));
        });

    console.log(json)
}

$('#picker-start').dateTimePicker({
    positionShift: { top: 0, left: 0 },
    title: "Select Date and Time",
    buttonTitle: "Select",
});

$('#picker-end').dateTimePicker({
    positionShift: { top: 0, left: 0 },
    title: "Select Date and Time",
    buttonTitle: "Select",
});