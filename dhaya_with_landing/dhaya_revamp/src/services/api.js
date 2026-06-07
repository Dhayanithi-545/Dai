import axios
from "axios";

const API =
  axios.create({

    baseURL:
    "http://localhost:8000"
  });

export const sendMessage =
  async (
    message
  ) => {

    const response =
      await API.post(
        "/chat/",
        {
          message
        }
      );

    return response.data;
};