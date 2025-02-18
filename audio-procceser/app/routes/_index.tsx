import type { MetaFunction } from "@remix-run/node";
import PolygonDivider from '~/components/icons/PolygonDivider.jsx';
import TearBottomDivider from '~/components/icons/TearBottomDivider.jsx';
import { NavLink } from "@remix-run/react";
import { format } from "mysql2";

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
    const currentYear = new Date().getFullYear();
  return (
      <div className="">
          <div className="flex flex-row justify-center dark:bg-gray-950">
              <div className="main"></div>
              <span className="emo-logo my-16 mb-28 mx-20"></span>
          </div>
          <PolygonDivider/>
          <div className="background-gradient flex flex-row md:flex-col sm:flex-col items-center contain">
              <div className=" flex flex-row justify-center p-5 w-[200px] gap-10 mt-28">
                  <img
                      src="/true-emos-logo-3.webp"
                      alt="Remix"
                      className="logo w-full"
                  />
              </div>
              <div className="flex flex-col items-center gap-6">
                  <h1 className="text-3xl font-bold">Welcome to True Emos</h1>
                  <span className="text-2xl font-bold">Where Emotions Speak the Truth</span>
                  {/* <span className="text-2xl font-bold">Speech-to-Text and Emotion Recognition from Audio</span> */}
                  <nav className="flex flex-col items-center gap-10 py-10">
                      <NavLink to="/traning-model" className="px-4 py-2 border text-white-500 border-gray-950 rounded-lg">Train Model</NavLink>
                      <NavLink to="/audio-recorder" className="px-4 py-2 border text-white-500 border-gray-950 rounded-lg">Record Audio</NavLink>
                      <NavLink to="/audio-upload" className="px-4 py-2 border text-white-500 border-gray-950 rounded-lg">Upload Audio</NavLink>
                      <NavLink to="/about" className="px-4 py-2 border text-white-500 border-gray-950 rounded-lg">About True Emos</NavLink>
                  </nav>
              </div>
          </div>
          {/* <TearBottomDivider/> */}
            <footer className="customer-experience">
                <svg width="100%" height="100%" viewBox="0 0 1280 140" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" className="tear-bottom">
                    <g fill="#fff" >
                        <path d="M0 51.76c36.21-2.25 77.57-3.58 126.42-3.58 320 0 320 57 640 57 271.15 0 312.58-40.91 513.58-53.4V0H0z" fillOpacity=".3"></path>
                        <path d="M0 24.31c43.46-5.69 94.56-9.25 158.42-9.25 320 0 320 89.24 640 89.24 256.13 0 307.28-57.16 481.58-80V0H0z" fillOpacity=".5"></path>
                        <path d="M0 0v3.4C28.2 1.6 59.4.59 94.42.59c320 0 320 84.3 640 84.3 285 0 316.17-66.85 545.58-81.49V0z"></path>
                    </g>
                </svg>
                <div className="footer">
                    <p>© {currentYear} True Emos – Feel the Real Emotion. </p>
                </div>
            </footer>
      </div>
    );
}
