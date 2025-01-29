import type { MetaFunction } from "@remix-run/node";
import AudioRecorder from '~/components/AudioRecorder.jsx';
import AudioUpload from '~/components/AudioUpload.jsx';
import PolygonDivider from '~/components/icons/PolygonDivider.jsx';

export const meta: MetaFunction = () => {
  return [
    { title: "New Remix App" },
    { name: "description", content: "Welcome to Remix!" },
  ];
};

export default function Index() {
  return (
      <div className="">
        <div className="flex flex-row justify-center">
          <span className="emo-logo my-16 mb-28 mx-20"></span>

        </div>
        <PolygonDivider />
        <div className="background-gradient flex flex-row md:flex-col sm:flex-col items-center ">
          <div className="container flex flex-row justify-center p-5 w-[200px] gap-10 mt-28">
            <img
                src="/true-emos-logo-3.webp"
                alt="Remix"
                className="logo w-full"
            />
          </div>
          <div className="container">
            <div className="flex flex-col items-center gap-6">
              <h1 className="text-4xl font-bold">Welcome to True Emos</h1>
              <span className="text-2xl font-bold">Speech-to-Text and Emotion Recognition from Audio</span>
            </div>
            <div className="flex flex-row justify-center gap-20 py-20">
              <AudioRecorder/>
              <AudioUpload/>
            </div>
          </div>
        </div>
      </div>
  );
}
