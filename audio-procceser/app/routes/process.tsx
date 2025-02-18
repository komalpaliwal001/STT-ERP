import axios from 'axios';
import {json, unstable_parseMultipartFormData, unstable_createFileUploadHandler, TypedResponse} from "@remix-run/node";

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