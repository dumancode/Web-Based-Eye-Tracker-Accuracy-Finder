let eyeTrackingData = [];
window.onload = async function() {
// Initialize an array to store the data
let isRecording = false;
    //start the webgazer tracker
    await webgazer.setRegression('ridge') /* currently must set regression and tracker */
        //.setTracker('clmtrackr')
        .setGazeListener(function(data, clock) {
            if (data && data.x !== null && data.y !== null) {
                if (!isRecording) {
                    isRecording = true;
                    }
               // console.log(data);
               // console.log(clock);
                     eyeTrackingData.push([data.x, data.y, clock]); // Push x, y, and clock values into the data array
                    } else {

                         isRecording = false;
                         }
        })
        .saveDataAcrossSessions(true)
        .begin();
        webgazer.showVideoPreview(false) /* shows all video previews */
            .showPredictionPoints(true) /* shows a square every 100 milliseconds where current prediction is */
            .applyKalmanFilter(true); /* Kalman Filter defaults to on. Can be toggled by user. */

    //Set up the webgazer video feedback.
    var setup = function() {

        //Set up the main canvas. The main canvas is used to calibrate the webgazer.
        var canvas = document.getElementById("plotting_canvas");
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        canvas.style.position = 'fixed';
    };
    setup();

};
function saveDataToCSV(data) {
    if (data.length === 0) {
        console.log("No data to save.");
        return;
    }

    // CSV formatına dönüştürmek için bir yardımcı işlev
    function convertToCSV(data) {
        const header = ['x', 'y', 'clock'];
        const csv = [header, ...data];
        return csv.map(row => row.join(',')).join('\n');
    }

    const csvContent = convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Dosyayı indirmek için bir indirme bağlantısı oluşturun
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'eye_track_values.csv';


    // Bağlantıyı tıklamak için otomatik olarak bir olay oluşturun
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: false,
    });
    a.dispatchEvent(clickEvent);

    // Kullanılmayan URL'yi temizleyin
    URL.revokeObjectURL(url);
}
function saveDataToCSV(data) {
    if (data.length === 0) {
        console.log("No data to save.");
        return;
    }

    // CSV formatına dönüştürmek için bir yardımcı işlev
    function convertToCSV(data) {
        const header = ['x', 'y', 'clock'];
        const csv = [header, ...data];
        return csv.map(row => row.join(',')).join('\n');
    }

    const csvContent = convertToCSV(data);
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Dosyayı indirmek için bir indirme bağlantısı oluşturun
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'eye_track_values.csv';


    // Bağlantıyı tıklamak için otomatik olarak bir olay oluşturun
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: false,
    });
    a.dispatchEvent(clickEvent);

    // Kullanılmayan URL'yi temizleyin
    URL.revokeObjectURL(url);
}

document.getElementById('finishButton').addEventListener('click', function() {


    saveDataToCSV(eyeTrackingData)
    //verileri sunucuya POST isteği ile gönder
        fetch('/save_data', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({ eyeTrackingData}) //verilerini isteğin gövdesine ekleyin
        })
        .then(response => {
            if (response.ok) {
                console.log("data has been successfully saved.");
                // Sunucudan gelen yanıtı işleyebilirsiniz (örneğin, başarılı bir yanıt veya hata mesajı).
            } else {
                console.error("Failed to save data.");
            }
        })
        .catch(error => {
            console.error("An error occurred while saving CSV data:", error);
        });




});

function saveDataToServer(azalmaOrani, widthRatio, testID) {
    // Save and send data to server
    fetch('/save_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ eyeTrackingData, azalmaOrani, widthRatio, testID }) // Add data to the request body
    })
    .then(response => {
        if (response.ok) {
            console.log("Data has been successfully saved.");
            // Handle the response from the server (e.g., success message or error handling).
        } else {
            console.error("Failed to save data.");
        }
    })
    .catch(error => {
        console.error("An error occurred while saving data to the server:", error);
    });
}

// Set to true if you want to save the data even if you reload the page.
window.saveDataAcrossSessions = true;

window.onbeforeunload = function() {
    webgazer.end();
}

/**
 * Restart the calibration process by clearing the local storage and reseting the calibration point
 */
function Restart(){
    document.getElementById("Accuracy").innerHTML = "<a>Not yet Calibrated</a>";
    webgazer.clearData();
    ClearCalibration();
    PopUpInstruction();
}
