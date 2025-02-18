import { useState, useRef, useEffect, ChangeEvent } from 'react';
import { useFetcher } from '@remix-run/react';
import { AudioVisualizer } from 'react-audio-visualize';
import ReactAudioPlayer from 'react-audio-player';

export default function AudioUpload() {
    const fetcher = useFetcher();
    const [blob, setBlob] = useState<Blob | null>(null);
    const [emotion, setEmotion] = useState<string | null>(null);
    const [text, setText] = useState<string | null>(null);
    const visualizerRef = useRef<HTMLCanvasElement>(null);
    console.log(fetcher)
    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setBlob(e.target.files[0]);
            setEmotion(null);
            setText(null);
        }
    };

    // Use useEffect to update state only when fetcher.data changes
    useEffect(() => {
        if (fetcher.data) {
            setEmotion(fetcher.data.emotion || null);
            setText(fetcher.data.text || null);
        }
    }, [fetcher.data]); 


    return (
        <div className="w-full background-gradient">
            <section className="flex flex-col items-center justify-center gap-10">
                <h3 className="h3 text-3xl">Upload Audio</h3>
                <fetcher.Form action="/process" method="post" encType="multipart/form-data">
                    <div className=" flex flex-col p-2 gap-6">
                        <div className="input-group relative">
                            <input className="peer fileinput"
                                name="audio_file"
                                type="file"
                                accept="audio/*"
                                onChange={handleFileChange}
                            />
                            <label className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md">
                                Select Audio
                            </label>
                        </div>
                        <div className="input-group relative">
                            <select name='model' className="peer w-full border border-[#1d2427]" >
                                <option value="">-- Select Model Type --</option>
                                <option value="svm">Support Vector Machine</option>
                                <option value="rf">Random Forest</option>
                                <option value="dt">Decision Tree</option>
                            </select>
                            <label className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md ">
                                Model Selection
                            </label>
                        </div>
                        {/* <input 
                            name="route"
                            type="hidden"
                            value="process"
                        /> */}
                        <button
                            type="submit"
                            title="Upload Recording"
                            className="btn-default input-group-btn p-2 rounded-lg"
                        >
                            {fetcher.state === 'submitting' ? 'Submitting...' : 'Submit'}
                        </button>
                    </div>
                </fetcher.Form>
                {(emotion && blob) && (
                    <>
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
                        <ReactAudioPlayer src={blob ? URL.createObjectURL(blob) : undefined} controls />
                    </>
                )}
                {emotion &&
                    <div className='emot'>
                        <div className={`emot ${emotion}`} ></div>
                    </div>
                }
                {text &&
                    <div className='text'>
                        {text}
                    </div>
                }
                <div>{fetcher?.error ? fetcher?.error : null}</div>
            </section>
        </div>
    );
};
