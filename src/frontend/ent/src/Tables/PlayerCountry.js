import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";


function PlayerCountry() {
    
    const [selectedCountry, setSelectedCountry] = useState("");
    const [result, setLista] = useState([]);
    const [procData, setProcData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20001/api/getJogadorPais')
            .then(response => response.json())
            .then(data => {
                let keys = ["id", "name", "age", "overall", "country"];
                let result = data.map(item => item.reduce((acc, val, i) => Object.assign(acc, { [keys[i]]: val }), {}));
                console.log(result);
                setLista(result);
                setProcData(null);
                if (selectedCountry) {
                    setTimeout(() => {
                        setProcData(result.filter(t => t.country === selectedCountry));
                    }, 500);
                }
            });
    }, [selectedCountry])
    const countries = result ? [...new Set(result.map(element => element.country))].sort() : [];
    return (
        <>
            <h1>Jogadores de País</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedCountry(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                countries.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
                            }
                        </Select>
                    </FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                    <ul>
                    {
                        procData.map(data => (
                            <li>
                                <div>Name: {data.name}</div>
                                <div>Age: {data.age}</div>
                                <div>Overall: {data.overall}</div>
                            </li>
                        ))
                    }
                    </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default PlayerCountry;

