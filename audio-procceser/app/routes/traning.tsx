import { useState, useRef } from 'react';
import { Form, useActionData } from '@remix-run/react';
import axios from 'axios';
import { json, unstable_parseMultipartFormData, unstable_createFileUploadHandler } from "@remix-run/node";

export const action = async ({ request }) => {
  const uploadHandler = unstable_createFileUploadHandler({
    directory:  "../uploads",
    maxFileSize: 1024 * 1024 * 10 // 10 MB
  });
  const formData = await unstable_parseMultipartFormData(request, uploadHandler);
  const file = formData.get("file");

    try {
      console.log(file, formData)
      // Send file to FastAPI
      const response = await axios.post("http://localhost:5003/training", formData, {
        headers: { "Content-Type": "multipart/form-data" }, // Axios auto-sets boundary
      });
  
      return json(response.data);
    } catch (error) {
      console.error("Error processing file:", error.response?.data || error.message);
      return json({ error: "Training get failed" }, { status: 500 });
    }
};

export default function Training() {
    const actionData = useActionData();

    return (
        <div className="w-full background-gradient">
            <section className="flex flex-col items-center justify-center gap-10">
                <h3 className="h3 text-3xl">Training Model</h3>
                <Form method="post" encType="multipart/form-data">
                    <div className="flex flex-col p-2 gap-6">
                        <div className="input-group relative">
                            <input
                                className="peer fileinput"
                                name='file'
                                type="file"
                                accept="csv/*"
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

                        <button
                            type="submit"
                            title="Upload Recording"
                            className="btn-default input-group-btn p-2 rounded-lg"
                        >
                            Submit
                        </button>
                    </div>
                </Form>
                {actionData?.message && <div>{actionData?.message}</div>}
            </section>
        </div>
    );
};
