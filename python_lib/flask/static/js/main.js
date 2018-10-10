// var checkbox = document.getElementById('tzTran')
var all = document.getElementsByClassName('timeconvert')

// checkbox.addEventListener( 'change', function() {
//     if(this.checked) {
//         for (var i = 0; i < all.length; i++){
//             all[i].dataset.ogTime = all[i].innerHTML
//             tzsplit = all[i].innerHTML.split('+')
//             timesplit = all[i].innerHTML.split(':')
//             all[i].dataset.tz = tzsplit[1]
//             all[i].innerHTML = tzsplit[0]
//             tzarray = tzsplit[1].split('')
//             tzhour = tzarray[0] + tzarray[1]
//             tzmin = tzarray[2] + tzarray[3]

//             nHour = parseInt(timesplit[0]) + parseInt(tzhour)
//             nMin = parseInt(timesplit[1]) + parseInt(tzmin)
//             if(nMin > 59){
//                 nHour++
//                 nMin -= 60
//             }
            
//             var newstr = addZeroBefore(nHour) + ':' + addZeroBefore(nMin) + ':' + tzsplit[0].split(':')[2]
//             all[i].innerHTML = newstr
//         }
//     } else {
//         for (var i = 0; i < all.length; i++){
//             if(all[i].dataset.tz != undefined){
//                 timesplit = all[i].innerHTML.split(':')
//                 var newstr = (parseInt(timesplit[0] - all[i].dataset.tz.slice(0, -2))) + ':' + timesplit[1] + ':' + timesplit[2]
//                 all[i].innerHTML = all[i].dataset.ogTime
//             }
//         }
//     }
// });

function converttime_print(x){
    time = x.split('T')[1]
    newTime = ''
    if(x.includes('+')){
        tz = time.split('+')
        timesplit = tz[0].split(':')
        temp = tz[1].split('')
        tzhour = temp[0] + temp[1]
        tzmin = temp[2] + temp[3]

        newHour = parseInt(timesplit[0]) + parseInt(tzhour) 
        newMin = parseInt(timesplit[1]) + parseInt(tzmin)

        if(newMin > 59){
            newHour++
            newMin -= 60
        }

        if(newMin < 10){
            newMin = '0' + newMin
        }

        if(newHour < 10){
            newHour = '0' + newHour
        }

        newTime = newHour + ':' + newMin
    }else if(x.includes('-')){
        tz = time.split('-')
        timesplit = tz[0].split(':')
        temp = tz[1].split('')
        tzhour = temp[0] + temp[1]
        tzmin = temp[2] + temp[3]

        newHour = parseInt(timesplit[0]) - parseInt(tzhour) 
        newMin = parseInt(timesplit[1]) - parseInt(tzmin)

        if(newMin < 59){
            newHour--
            newMin += 60
        }

        if(newMin < 10){
            newMin = '0' + newMin
        }

        if(newHour < 10){
            newHour = '0' + newHour
        }

        newTime = newHour + ':' + newMin
    }
    return newTime
}

function converttime(x){
    time = x.split('T')[1]
    newTime = ''
    if(x.includes('+')){
        tz = time.split('+')
        timesplit = tz[0].split(':')
        temp = tz[1].split('')
        tzhour = temp[0] + temp[1]
        tzmin = temp[2] + temp[3]

        newHour = parseInt(timesplit[0]) + parseInt(tzhour) 
        newMin = parseInt(timesplit[1]) + parseInt(tzmin)

        if(newMin > 59){
            newHour++
            newMin -= 60
        }
        newTime = newHour + ':' + newMin
    }else if(x.includes('-')){
        tz = time.split('-')
        timesplit = tz[0].split(':')
        temp = tz[1].split('')
        tzhour = temp[0] + temp[1]
        tzmin = temp[2] + temp[3]

        newHour = parseInt(timesplit[0]) - parseInt(tzhour) 
        newMin = parseInt(timesplit[1]) - parseInt(tzmin)

        if(newMin < 59){
            newHour--
            newMin += 60
        }
        newTime = newHour + ':' + newMin
    }
    newTime = x.split('T')[0] + 'T' + newTime
    return newTime
}

function removeDiv(className){
    var elem = document.getElementsByClassName(className)
    for (var i = elem.length - 1; i >= 0; --i) {
        elem[i].remove();
    }
}