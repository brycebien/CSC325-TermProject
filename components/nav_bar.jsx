import Link from "next/link";
import { useEffect, useState, useCallback } from "react";
import { useSession } from "next-auth/react";
import { signOut } from "next-auth/react";
import { useRouter } from "next/router";
import { Router } from "react-router-dom";

function NavBar() {
  const router = useRouter();
  const { data: session } = useSession();
  const [profileData, setProfileData] = useState([]);
  const [selectedOption, setSelectedOption] = useState(null);

  const getProfileData = useCallback(async () => {
    if (session && session.accessToken) {
      const response = await fetch("https://api.spotify.com/v1/me", {
        headers: {
          Authorization: `Bearer ${session.accessToken}`,
        },
      });
      const data = await response.json();
      setProfileData(data);
    }
  }, [session]);

  useEffect(() => {
    getProfileData();
  }, [getProfileData]);

  useEffect(() => {
    setSelectedOption(localStorage.getItem("selectedOption"));
  }, []);

  return (
    <header className="header top-0 bg-gray-900 shadow-md flex items-center justify-between px-8 py-02 z-1">
      <h1 className="w-3/12">
        <div
          className="flex items-center cursor-pointer"
          onClick={() => {
            setSelectedOption((prev) => {
              const newValue = "Profile";
              localStorage.setItem("selectedOption", newValue);
              return newValue;
            });
            router.push("/");
          }}
        >
          <svg
            width="160px"
            height="60px"
            viewBox="0 0 48 48"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g id="SVGRepo_bgCarrier" strokeWidth="0"></g>
            <g
              id="SVGRepo_tracerCarrier"
              strokeLinecap="round"
              strokeLinejoin="round"
            ></g>
            <g id="SVGRepo_iconCarrier">
              {" "}
              <rect width="48" height="48" fill="gray-900"></rect>{" "}
              <path
                d="M42 30V24.4615C42 14.2655 33.9411 6 24 6C14.0589 6 6 14.2655 6 24.4615V30"
                stroke="#000000"
                strokeWidth="4"
                strokeLinecap="round"
                strokeLinejoin="round"
              ></path>{" "}
              <path
                d="M34 32C34 29.7909 35.7909 28 38 28H42V42H38C35.7909 42 34 40.2091 34 38V32Z"
                fill="#1DB954"
                stroke="#000000"
                strokeWidth="4"
                strokeLinejoin="round"
              ></path>{" "}
              <path
                d="M42 32H44C45.1046 32 46 32.8954 46 34V36C46 37.1046 45.1046 38 44 38H42V32Z"
                fill="#000000"
              ></path>{" "}
              <path
                d="M6 32H4C2.89543 32 2 32.8954 2 34V36C2 37.1046 2.89543 38 4 38H6V32Z"
                fill="#000000"
              ></path>{" "}
              <path
                d="M6 28H10C12.2091 28 14 29.7909 14 32V38C14 40.2091 12.2091 42 10 42H6V28Z"
                fill="#1DB954"
                stroke="#000000"
                strokeWidth="4"
                strokeLinejoin="round"
              ></path>{" "}
            </g>
          </svg>
        </div>
      </h1>
      <nav className="nav font-semibold text-lg">
        <ul className="flex items-center">
          <li
            className={`p-4 border-b-2 ${
              selectedOption === "Profile"
                ? "border-green-500 text-green-500"
                : "border-green-500 border-opacity-0"
            } hover:border-opacity-100 hover:text-green-500 duration-200 cursor-pointer`}
            onClick={() => {
              setSelectedOption((prev) => {
                const newValue = "Profile";
                localStorage.setItem("selectedOption", newValue);
                return newValue;
              });
              router.push("/");
            }}
          >
            Recommender
          </li>
        </ul>
      </nav>
      <div className="w-3/12 flex justify-end">
        <button
          className="text-white px-4 py-2 rounded-full bg-green-500 font-bold text-lg align"
          onClick={() => signOut("spotify", { callbackUrl: "/login" })}
        >
          Logout
        </button>
        <div className="avatar pl-5">
          <div className="w-12 rounded-xl">
            <img
              src={
                profileData.images && profileData.images.length > 1
                  ? profileData.images[1].url
                  : "https://upload.wikimedia.org/wikipedia/commons/b/b5/Windows_10_Default_Profile_Picture.svg"
              }
              alt="user image"
            />
          </div>
        </div>
      </div>
    </header>
  );
}

export default NavBar;
