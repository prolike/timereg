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
    const url = "http://localhost:5000/addtime"
    const other = {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({issue: issueID.value, start_time: res1.value, end_time: res2.value, username: 'davidcarl'})
    }
    fetch(url, other)
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            console.log(JSON.stringify(myJson));
        });

    // console.log(json)
}