import Players from "../Tables/Players";
import Country from "../Tables/Country";

const Sections = [

    {
        id: "players",
        label: "Players",
        content: <Players/>
    },

    {
        id: "country",
        label: "Country",
        content: <Countries/>
    },

    {
        id: "countries",
        label: "Countries",
        content: <h1>Countries - Work in progress</h1>
    }

];

export default Sections;