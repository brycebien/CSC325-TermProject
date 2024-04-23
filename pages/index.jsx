import NavBar from "@/components/nav_bar";
import { useSession } from "next-auth/react";
import React, { useEffect, useState, useCallback } from "react";

export default function Home() {
  const { data: session } = useSession();
  const [searchResults, setSearchResults] = useState([]);
  const [resultsDisplay, setResultsDisplay] = useState(null);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [selectedTrackFeatures, setSelectedTrackFeatures] = useState(null);

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
      const data = await response.json();
      return data;
    }
  }

  async function handleItemClick(itemId) {
    const selectedTrack = searchResults.find((track) => track.id === itemId);
    setSelectedTrack(selectedTrack);
    if (session && session.accessToken) {
      const response = await fetch(
        `https://api.spotify.com/v1/audio-features/${itemId}`,
        {
          headers: {
            Authorization: `Bearer ${session.accessToken}`,
          },
        }
      );
      setSearchResults([]);
      setSelectedTrackFeatures(await response.json());
      document.getElementById("my_modal_3").close();
      if (selectedTrackFeatures) {
        fetch("http://localhost:5000/receive_data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(selectedTrackFeatures),
        });
      }
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
                  <tr key={index} onClick={() => handleItemClick(track.id)}>
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
      <div className="pt-20 pl-20 pr-20">
        <div className="flex flex-col">
          <div className="table-container">
            <button
              className="btn"
              onClick={() => document.getElementById("my_modal_3").showModal()}
            >
              Select Track to Get Recommendations
            </button>
            <dialog
              id="my_modal_3"
              className="modal"
              onClose={() => setSearchResults([])}
            >
              <div className="modal-box max-w-5xl">
                <form method="dialog">
                  <button
                    className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2"
                    onClick={() => {
                      document.getElementById("my_modal_3").close();
                      setSearchResults([]);
                    }}
                  >
                    ✕
                  </button>
                </form>
                <h3 className="font-bold text-lg">Search for a track</h3>
                <input
                  type="text"
                  id="searchTerm"
                  className="input"
                  placeholder="Enter track name"
                />
                <button
                  className="btn"
                  onClick={() => {
                    const searchTerm =
                      document.getElementById("searchTerm").value;
                    if (searchTerm) {
                      searchItem(searchTerm, "track").then((data) => {
                        setSearchResults(data.tracks.items);
                      });
                    }
                  }}
                >
                  Search
                </button>
                {resultsDisplay}
              </div>
            </dialog>
            {selectedTrack && (
              <>
                <div className="font-bold pt-20">Selected Track:</div>
                <table className="table">
                  <thead>
                    <tr>
                      <th className="text-left px-12"></th>
                      <th className="text-left px-12">Track</th>
                      <th className="text-left px-12">Artist</th>
                      <th className="text-left px-12">Album</th>
                      <th className="text-left px-12"></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>
                        <div className="flex items-center gap-3">
                          <div className="avatar">
                            <div className="w-12 h-12">
                              <img
                                src={
                                  selectedTrack.album
                                    ? selectedTrack.album.images[0].url
                                    : "https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg"
                                }
                                alt="album_img"
                              />
                            </div>
                          </div>
                          <div className="font-bold">{selectedTrack.name}</div>
                        </div>
                      </td>
                      <th>
                        <div className="font-bold">
                          {selectedTrack.artists[0].name}
                        </div>
                      </th>
                      <th>
                        <div className="font-bold">
                          {selectedTrack.album.name}
                        </div>
                      </th>
                    </tr>
                  </tbody>
                </table>
              </>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
