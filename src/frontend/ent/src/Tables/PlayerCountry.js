import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";






function JogadorPais() {
    
    const [selectedCountry, setSelectedCountry] = useState("");
    const [listaJP, setLista] = useState(null);
    const [procData, setProcData] = useState(null);

    useEffect(() => {fetch('http://localhost:20001/api/getJogadorPais')
    .then(response => response.json())
    .then(data => {
      let keys = ["id", "name", "age", "overall", "country"];
      let result = data.map(item => item.reduce((acc, val, i) => Object.assign(acc, { [keys[i]]: val }), {}));
      listaJP=result
      setLista(result)
    });
    setProcData(null);
        if (selectedCountry) {
            setTimeout(() => {
                setProcData(listaJP.filter(t => t.country === selectedCountry));
            }, 500);
        }
    }, [selectedCountry])
    const countries = [...new Set(listaJP.map(element => element.country))].sort();
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
                                procData.map(data => <li>{data.country}</li>)
                            }
                        </ul> :
                        selectedCountry ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default JogadorPais;

