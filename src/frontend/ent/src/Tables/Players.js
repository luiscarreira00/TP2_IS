import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


function Players() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [result, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);

    useEffect(() => {
        fetch('http://localhost:20001/api/data')
          .then(response => response.json())
          .then(data => {
            let keys = ["id", "name", "age", "overall"];
            let result = data.map(item => item.reduce((acc, val, i) => Object.assign(acc, { [keys[i]]: val }), {}));
            result.sort((a, b) => a.id - b.id);
            console.log(result);
            setData(result);
            setMaxDataSize(result.length);
          });
    }, []);

    

    return (
        <>
            <h1>Players</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Player Name</TableCell>
                            <TableCell align="center">Age</TableCell>
                            <TableCell align="center">Overall</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {      
                            result ?
                                result.map((item) => (
                                    <TableRow
                                        key={item.name}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{item.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {item.name}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {item.age}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {item.overall}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }


        </>
    );
}

export default Players;
