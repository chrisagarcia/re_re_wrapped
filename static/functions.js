// this is just to declutter my html

export function resetter (id) {
    let element = document.getElementById(id);

    while (element.firstElementChild) {
        element.firstElementChild.remove();
    }

};

export function rollingFill (track) {
    
    if (track) {

        let button = document.getElementById('tracks-more-button');

        if (button.textContent === "Show More") {
            tableFill(trackCell, tracksJSON, trackTable, 50);
            button.textContent = "Show Less";
        } else  if (button.textContent === "Show Less") {
            tableFill(trackCell, tracksJSON, trackTable, 10);
            button.textContent = "Show More"
        };
        
    } else {

        let button = document.getElementById('artists-more-button');

        if (button.textContent === "Show More") {
            tableFill(artistCell, artistsJSON, artistTable, 50);
            button.textContent = "Show Less";
        } else  if (button.textContent === "Show Less") {
            tableFill(artistCell, artistsJSON, artistTable, 10);
            button.textContent = "Show More"
        };
    }
};

export function listFill(listItemFunction, jsonData, parentContainer, listLength) {
    
    for (let i = 0; i < listLength; i++) {
        listItemFunction(jsonData[i], parentContainer);
    };

};

export function trackCell (individualTrack) {
    let cell = document.createElement("TD");
    let cellContainer = document.createElement("DIV");
    let cover = document.createElement("IMG");
    let textContainer = document.createElement("DIV");
    let song = document.createElement("SPAN");
    let artist = document.createElement("P");

    cover.src = individualTrack["img"];

    // styling
    cover.width = 200;
    cover.height = 200;
    cover.className = "album-art";

    let trackString = individualTrack["song"].slice(0, 25);

    song.appendChild(document.createTextNode(trackString));
    artist.appendChild(document.createTextNode(individualTrack["artists"][0]));

    textContainer.appendChild(song);
    textContainer.appendChild(artist);

    cellContainer.appendChild(cover);
    cellContainer.appendChild(textContainer);

    cell.appendChild(cellContainer);

    return cell
};

export function artistCell (individualArtist) {
    let cell = document.createElement("TD");
    let cellContainer = document.createElement("DIV");
    let cover = document.createElement("IMG");
    let textContainer = document.createElement("DIV");
    let artist = document.createElement("SPAN");
    let popularity = document.createElement("p");

    cover.src = individualArtist["img"];

    // image styling
    cover.width = 200;
    cover.height = 200;
    cover.className = "artist-image";
    
    // adding text
    artist.appendChild(document.createTextNode(individualArtist["artist"]));
    popularity.appendChild(document.createTextNode("Popularity: " + individualArtist["popularity"]));
    
    textContainer.appendChild(artist);
    textContainer.appendChild(popularity);
    cellContainer.append(cover);
    cellContainer.appendChild(textContainer);
    cell.appendChild(cellContainer);

    return cell
};

export function tableFill(cellFiller, jsonData, parentContainer, listLength) {

    for (let i=0; i<listLength; i++) {
        if (jsonData[i]) {

            if (i % 3 === 0) {
                var row = document.createElement("TR");
                parentContainer.appendChild(row);
            };

            // fill in the list function parameters
            let cell = cellFiller(jsonData[i]);
            row.appendChild(cell);
        };
    };
};

// makes a few of the features Histograms
export function histogram(featureData, parent) {

    let data = {
        'key': [],
        'loudness': [],
        'tempo': [],
        'danceability': [],
        'energy': [],
        'speechiness': [],
        'acousticness': [],
        'instrumentalness': [],
        'liveness': [],
        'valence': []
    };

    featureData.forEach(track => {
        Object.keys(data).forEach(feature => {
            data[feature].push(track[feature]);
        });
    });

    let keys = Object.keys(data)

    for (let i = 0; i < keys.length; i++) {

        let histBox = document.createElement('DIV');
        let histogram = document.createElement('DIV');
        let key = keys[i];

        histBox.appendChild(histogram);
        parent.appendChild(histBox);

        let trace = {
            x: data[key],
            type: 'histogram',
        };
        
        let layout = {
            bargroupgap: 0.01, 
            title: (key.charAt(0).toUpperCase() + key.slice(1)), 
            xaxis: {title: "Value"}, 
            yaxis: {title: "Count"}
        };
        Plotly.newPlot(histogram, [trace], layout);

    };
};