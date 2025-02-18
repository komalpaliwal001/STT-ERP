import axios from 'axios';
import {json, unstable_parseMultipartFormData, unstable_createFileUploadHandler, TypedResponse} from "@remix-run/node";

export async function action ({ request } : {request: Request}) : Promise<TypedResponse> {
  const uploadHandler = unstable_createFileUploadHandler({
    directory:  "../uploads",
    maxPartSize: 1024 * 1024 * 10 // 10 MB
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
      console.error("Error processing file:", error);
      return json({ error: "Training get failed" }, { status: 500 });
    }
};