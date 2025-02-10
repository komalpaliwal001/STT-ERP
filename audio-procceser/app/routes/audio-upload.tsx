import {useState, useRef, ChangeEvent} from 'react';
import { Form, useActionData } from '@remix-run/react';
import axios from 'axios';
import {json, unstable_parseMultipartFormData, unstable_createFileUploadHandler, TypedResponse} from "@remix-run/node";
import { AudioVisualizer } from 'react-audio-visualize';

export async function action ({ request } : {request: Request}) : Promise<TypedResponse> {
  const uploadHandler = unstable_createFileUploadHandler({
    directory:  "../uploads", maxPartSize: 1024 * 1024 * 10 // 10 MB
  });
  const formData = await unstable_parseMultipartFormData(request, uploadHandler);
    try {
      // Send file to FastAPI
      const response = await axios.post("http://localhost:5003/process", formData, {
        headers: { "Content-Type": "multipart/form-data" }, // Axios auto-sets boundary
      });

      return json(response.data);
    } catch (error) {
        if (error?.response?.status === 404) {
            console.error("Error processing file:", error?.response?.data || error?.message);
            return json({ error: "Failed to access audio" }, { status: 404 });
        } else {
            console.error("Error processing file:", error?.response?.data || error?.message);
            return json({ error: "Failed to process audio" }, { status: 500 });
        }
    }
};

export default function AudioUpload() {
    const actionData = useActionData();
    const [blob, setBlob] = useState<Blob | null>(null);
    const visualizerRef = useRef<HTMLCanvasElement>(null);
    const emotion = actionData?.emotion;
    return (
        <div className="w-full background-gradient">
            <section className="flex flex-col items-center justify-center gap-10">
                <h3 className="h3 text-3xl">Upload Audio</h3>
                <Form method="post" encType="multipart/form-data">
                    <div className=" flex flex-col p-2 gap-6">
                        <div className="input-group relative">
                            <input className="peer fileinput"
                                name="audio_file"
                                type="file"
                                accept="audio/*"
                                onChange={(e: ChangeEvent<HTMLInputElement>) => {
                                    if (e.target.files && e.target.files.length > 0) {
                                        setBlob(e.target.files[0]); // Ensure a file is selected before accessing it
                                    }
                                }}
                            />
                            <label className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md">
                              Select Audio
                          </label>
                        </div>
                        <div className="input-group relative">
                            <select name='model' className="peer w-full border border-[#1d2427]">
                                <option value="">-- Select Model Type --</option>
                                <option value="svm">Support Vector Machine</option>
                                <option value="rf">Random Forest</option>
                                <option value="dt">Decision Tree</option>
                            </select>
                            <label
                                className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md ">
                                Model Selection
                            </label>
                        </div>
                        <button
                            type="submit"
                            title="Upload Recording"
                            className="btn-default input-group-btn p-2 rounded-lg"
                        >
                            {/*<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="3px" width="50" height="30" viewBox="0 0 48 48">*/}
                            {/*    <path*/}
                            {/*        d="M 24 2 C 19.04 2 15 6.04 15 11 L 15 26 C 15 30.28 17.999766 33.869297 22.009766 34.779297 C 22.014766 34.310297 22.053375 33.848625 22.109375 33.390625 C 22.125375 33.262625 22.145062 33.136766 22.164062 33.009766 C 22.211063 32.702766 22.271844 32.398609 22.339844 32.099609 C 23.317844 27.818609 26.405078 24.354797 30.455078 22.841797 C 30.682078 22.756797 30.909578 22.673562 31.142578 22.601562 C 31.376578 22.528562 31.613516 22.462344 31.853516 22.402344 C 32.230516 22.308344 32.609 22.213391 33 22.150391 L 33 11 C 33 6.04 28.96 2 24 2 z M 10.5 21 C 9.67 21 9 21.67 9 22.5 L 9 26 C 9 33.76 14.93 40.169922 22.5 40.919922 L 22.5 45.5 C 22.5 46.33 23.17 47 24 47 C 24.83 47 25.5 46.33 25.5 45.5 L 25.5 43.869141 C 24.7 43.009141 24.010938 42.040234 23.460938 40.990234 C 23.290938 40.660234 23.132734 40.325625 22.990234 39.984375 C 22.847734 39.643125 22.719375 39.294453 22.609375 38.939453 C 22.499375 38.589453 22.400312 38.240859 22.320312 37.880859 C 16.500312 37.070859 12 32.05 12 26 L 12 22.5 C 12 21.67 11.33 21 10.5 21 z M 35 24 C 28.925 24 24 28.925 24 35 C 24 41.075 28.925 46 35 46 C 41.075 46 46 41.075 46 35 C 46 28.925 41.075 24 35 24 z M 35 27 C 35.552 27 36 27.448 36 28 L 36 34 L 42 34 C 42.552 34 43 34.448 43 35 C 43 35.552 42.552 36 42 36 L 36 36 L 36 42 C 36 42.552 35.552 43 35 43 C 34.448 43 34 42.552 34 42 L 34 36 L 28 36 C 27.448 36 27 35.552 27 35 C 27 34.448 27.448 34 28 34 L 34 34 L 34 28 C 34 27.448 34.448 27 35 27 z"></path>*/}
                            {/*</svg>*/}
                            Submit
                        </button>
                    </div>
                </Form>
                {blob && (
                    <div className='audio-record'>
                      <AudioVisualizer
                        ref={visualizerRef}
                        blob={blob}
                        width={500}
                        height={75}
                        barWidth={1}
                        gap={0}
                        barColor={'#01BDAF'}
                      />
                  </div>
                )}
                {emotion &&
                  <div className='emotion-section w-[200px]'>
                    <div className={`emotions ${emotion}`} ></div>
                  </div>
                }
                <div>{actionData?.error ? actionData?.error : null}</div>
            </section>
        </div>
    );
};
