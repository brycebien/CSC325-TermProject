import NavBar from "@/components/nav_bar";
import { useSession } from "next-auth/react";
import React, { useEffect, useState, useCallback } from "react";

export default function Ratings() {
  const { data: session } = useSession();
  const [searchResults, setSearchResults] = useState([]);
  const [resultsDisplay, setResultsDisplay] = React.useState(null);

  async function searchItem(searchTerm, itemType) {
    if (session && session.accessToken && searchTerm) {
      const response = await fetch(
        `https://api.spotify.com/v1/search?q=${searchTerm}&type=${itemType}&limit=10`,
        {
          headers: {
            Authorization: `Bearer ${session.accessToken}`,
          },
        }
      );
      console.log(response);
      const data = await response.json();
      return data;
    }
  }

  useEffect(() => {
    if (searchResults && searchResults.length > 0) {
      const newDisplay = (
        <div>
          <p>Results:</p>
          <table className="table">
            <thead>
              <tr>
                <th className="text-left px-12">Track</th>
                <th className="text-left px-12">Artist</th>
                <th className="text-left px-12">Album</th>
              </tr>
            </thead>
            <tbody>
              {searchResults &&
                searchResults.map((track, index) => (
                  <tr
                    key={index}
                    onClick={() =>
                      handleItemClick(track.id, "tracks", "my_modal_3")
                    }
                  >
                    <td>
                      <div className="flex items-center gap-3">
                        <div className="avatar">
                          <div className="w-12 h-12">
                            <img
                              src={
                                track.album
                                  ? track.album.images[0].url
                                  : "https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg"
                              }
                              alt="album_img"
                            />
                          </div>
                        </div>
                        <div className="font-bold">{track.name}</div>
                      </div>
                    </td>
                    <th>
                      <div className="font-bold">{track.artists[0].name}</div>
                    </th>
                    <th>
                      <div className="font-bold">{track.album.name}</div>
                    </th>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      );
      setResultsDisplay(newDisplay);
    }
  }, [searchResults]);

  return (
    <main>
      <NavBar />
    </main>
  );
}
