import { useEffect, ChangeEvent } from 'react';
import { useFetcher } from '@remix-run/react';

export default function Training() {
    const fetcher = useFetcher();

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
           
        }
    };

    // Use useEffect to update state only when fetcher.data changes
    useEffect(() => {
        if (fetcher.data) {
            
        }
    }, [fetcher.data]); 

    return (
        <div className="w-full background-gradient">
            <section className="flex flex-col items-center justify-center gap-10">
                <h3 className="h3 text-3xl">Training Model</h3>
                <fetcher.Form action='/training' method="post" encType="multipart/form-data">
                    <div className="flex flex-col p-2 gap-6">
                        <div className="input-group relative">
                            <input
                                className="peer fileinput"
                                name='file'
                                type="file"
                                accept="csv/*"
                                onChange={handleFileChange}
                            />
                            <label
                                className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md">
                                Choose Datasets
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
                        <div className="input-group relative">
                            <textarea
                                className="peer w-full border border-[#1d2427]"
                                name='labels'
                                rows={5}
                                required
                                placeholder="{0: 'happy', 1: 'sad', 2: 'neutral'}"
                            ></textarea>
                            <label
                                className="absolute left-5 top-[-12px] px-3 bg-white text-[#1d2427] text-md">
                                Enter Labels
                            </label>
                        </div>
                        {/* <input 
                            name="route"
                            type="hidden"
                            value="training"
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
                {fetcher?.error && <div>{fetcher?.error}</div>}
            </section>
        </div>
    );
};
