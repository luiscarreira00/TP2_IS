import Players from "../Tables/Players";
import Countries from "../Tables/Country";
import PlayerCountry from "../Tables/PlayerCountry";

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
        id: "playerCountry",
        label: "playerCountry",
        content: <PlayerCountry/>
    }

];

export default Sections;