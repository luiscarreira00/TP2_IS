import React, {useEffect, useState} from 'react';
import {LayerGroup, useMap} from 'react-leaflet';
import {ObjectMarker} from "./ObjectMarker";

const DEMO_DATA = [
    {
        "type": "feature",
        "geometry": {
            "coordinates": [41.69662, -8.84979]
        },
        "properties": {
            id: 696969,
            name: "Messi",
            country: "Argentina",
        }
    }
];

function ObjectMarkersGroup() {

    const map = useMap();
    const [geom, setGeom] = useState([]);
    const [bounds, setBounds] = useState(map.getBounds());
    useEffect(() => {
            fetch('http://localhost:20002/api/markersJogadores')
            .then(response => response.json())
            .then(data => {
                console.log(data);
                setGeom(data)
            });
    }, [bounds])
    /**
     * Setup the event to update the bounds automatically
     */
    useEffect(() => {
        const cb = () => {
            setBounds(map.getBounds());
        }
        map.on('moveend', cb);

        return () => {
            map.off('moveend', cb);
        }
    }, [map]);

    /* Updates the data for the current bounds */
    

    return (
        <LayerGroup>
            {
                geom.map(geoJSON => <ObjectMarker key={geoJSON.properties.id} geoJSON={geoJSON}/>)
            }
        </LayerGroup>
    );
}

export default ObjectMarkersGroup;
